from fastapi import Request

from .IndexingService import IndexingService
from ...helpers.config import get_settings


class ElasticSearchService(IndexingService):
    def __init__(self, request: Request):
        self.es = request.app.es_client
        self.index_name = get_settings().ES_INDEXING

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
                body={
                    "mappings": {
                        "properties": {
                            "file_id": {"type": "keyword"},
                            "content": {"type": "keyword"}  # disables default Elastic preprocessing
                        }
                    }
                }
            )
            return True
        return False

    async def index(self, file_id: str, processed_content: str) -> bool:
        """
        Index a document in Elasticsearch.

        :param file_id: The ID of the file to index.
        :param processed_content: The processed content of the file.
        :return: True if the document was indexed successfully, False otherwise.
        """
        await self.create_index_if_not_exists()

        res = await self.es.index(
            index=self.index_name,
            id=file_id,
            document={
                "file_id": file_id,
                "content": processed_content
            }
        )

        return res['result'] == 'created' or res['result'] == 'updated'

    async def search(self, processed_query: str) -> list:
        '''
        Search for documents in Elasticsearch.

        :param processed_query: The cleaned search query.
        :return: A list of document IDs matching the search query.
        '''
        await self.create_index_if_not_exists()

        res = await self.es.search(
            index=self.index_name,
            body={
                "query": {
                    "term": {
                        "content": processed_query  # Search in the same field that was indexed
                    }
                }
            }
        )

        search_results = []
        for hit in res["hits"]["hits"]:
            search_results.append({
                "file_id": hit["_source"]["file_id"],
                "score": hit["_score"],
                "content": hit["_source"].get("content", "")  # Include content if needed
            })
        return search_results
