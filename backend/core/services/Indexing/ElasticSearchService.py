import numpy as np
from fastapi import Request

from .IndexingService import IndexingService
from ...helpers.config import get_settings


class ElasticSearchService(IndexingService):
    def __init__(self, request: Request):
        self.es = request.app.es_client
        self.index_name = get_settings().ES_INDEXING
        self.embedding_model = request.app.embedding_model

    async def create_index_if_not_exists(self):
        """
        Create the index with proper mappings if it doesn't exist.
        This ensures 'content' field is stored as keyword type to disable default preprocessing.
        """
        # Check if index exists
        exists = await self.es.indices.exists(index=self.index_name)

        if not exists:
            # Create index with explicit mappings
            await self.es.indices.create(
                index=self.index_name,
                mappings={
                    "properties": {
                        "file_id": {
                            "type": "text"
                        },
                        "embedding": {
                            "type": "dense_vector",
                            "similarity": "cosine",
                            "dims": 768,
                            "index": True
                        }
                    }
                }
            )
            return True
        return False

    async def index(self, file_id: str, file_content: str) -> bool:
        """
        Index a document in Elasticsearch.

        :param file_id: The ID of the file to index.
        :param file_content: The content of the file.
        :return: True if the document was indexed successfully, False otherwise.
        """
        await self.create_index_if_not_exists()

        res = await self.es.index(
            index=self.index_name,
            id=file_id,
            document={
                "file_id": file_id,
                "embedding": self.embedding_model.encode(file_content)
            }
        )

        return res['result'] == 'created' or res['result'] == 'updated'

    async def search(self, query: str, retrieved_count: int = 10, feedback_docs: int = 20,
                     alpha: float = 1, beta: float = 0.75, gamma: float = 0.15,
                     relevance_threshold: float = 0.25, min_score_threshold: float = 0.3) -> list:
        '''
        Search for documents in Elasticsearch.

        :param query: The search query.
        :param retrieved_count: The number of documents to retrieve.
        :param feedback_docs: The number of documents to use for feedback.
        :param alpha: Weight for the original query.
        :param beta: Weight for the feedback documents.
        :param gamma: Weight for the negative feedback documents.
        :param relevance_threshold: Percentage of top documents to consider as relevant
        :param min_score_threshold: The minimum score threshold for a document to be considered a match.
        :return: A list of document IDs matching the search query.
        '''
        await self.create_index_if_not_exists()

        async def search_by_vector(embedding_vector: list[float], k: int = 10):
            search_result = await self.es.knn_search(
                index=self.index_name,
                knn={
                    "field": "embedding",
                    "query_vector": embedding_vector,
                    "num_candidates": 500,
                    "k": k,
                }
            )

            return search_result['hits']['hits']

        query_vector = self.embedding_model.encode(query)

        # hits = [
        #     {
        #         "file_id": hit["_source"]["file_id"],
        #         "score": hit["_score"],
        #     }
        #     for hit in search_results
        # ]

        # Initial search to get feedback documents
        initial_hits = await search_by_vector(query_vector.tolist(), k=feedback_docs)

        scores = [hit['_score'] for hit in initial_hits]
        vectors = [np.array(hit['_source']['embedding']) for hit in initial_hits]

        # split documents to relevant and non-relevant
        sorted_scores = sorted(scores, reverse=True)
        feedback_docs_count = int(len(sorted_scores) * relevance_threshold)
        feedback_docs_count = max(feedback_docs_count, 1)

        relevant_vectors = vectors[:feedback_docs_count]
        non_relevant_vectors = vectors[feedback_docs_count:]

        # Apply ROCCHIO formula with numpy for vectorized operations
        modified_query = (alpha * query_vector
                          + beta * np.mean(relevant_vectors, axis=0)
                          - gamma * np.mean(non_relevant_vectors, axis=0))
        modified_query = modified_query / np.linalg.norm(modified_query)  # normalize

        # Final search with modified query
        final_hits = await search_by_vector(modified_query.tolist(), k=retrieved_count * 2)
        filtered_hits = [hit for hit in final_hits if hit['_score'] >= min_score_threshold]
        filtered_hits.sort(key=lambda x: x['_score'], reverse=True)

        final_result = [
            {
                "file_id": hit["_source"]["file_id"],
                "score": hit["_score"],
            }
            for hit in filtered_hits
        ]

        return final_result[:retrieved_count]
