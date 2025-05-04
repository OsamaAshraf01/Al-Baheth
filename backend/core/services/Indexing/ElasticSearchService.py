from fastapi import Request

from .IndexingService import IndexingService
from ...helpers.config import get_settings


class ElasticSearchService(IndexingService):
    def __init__(self, request: Request):
        self.es = request.app.es_client
        self.index_name = get_settings().ES_INDEXING

    async def index(self, file_id: str, content: str) -> bool:
        """
        Index a document in Elasticsearch.
        
        :param file_id: The ID of the file to index.
        :param content: The content of the document to index.
        """
        res = await self.es.index(index=self.index_name, id=file_id, body={"file_id": file_id, "content": content})

        if res['result'] == 'created':
            return True
        return False

    async def search(self, query: str) -> list:
        '''
        Search for documents in Elasticsearch.
        
        :param query: The search query.
        :return: A list of documents IDs matching the search query.
        '''
        res = await self.es.search(
            index=self.index_name,
            query={
                "match": {
                    "content": query
                }
            }
        )

        file_ids = [hit["_source"]["file_id"] for hit in res["hits"]["hits"]]
        return file_ids
