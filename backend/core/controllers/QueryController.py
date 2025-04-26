from controllers import BaseController
from repositories import DocumentRepo

class QueryController(BaseController):
    
    def __init__(self, document_repo: DocumentRepo):
        """
        Initialize the QueryController with a document repository.
        
        :param document_repo: An instance of DocumentRepo for querying documents.
        """
        super().__init__()
        self.document_repo = document_repo
    async def query(self, query):
        return await self.document_repo.search(query)