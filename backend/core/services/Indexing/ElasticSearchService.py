from fastapi import Request
from .IndexingService import IndexingService

class ElasticSearchService(IndexingService):
    def __init__(self, request: Request):
        self.es = request.app.es_client
        self.index_name = "docs"
    
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