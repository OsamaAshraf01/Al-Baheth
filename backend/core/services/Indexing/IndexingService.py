from abc import ABC, abstractmethod


class IndexingService(ABC):
    """
    Abstract base class for indexing services.
    """

    @abstractmethod
    async def index(self, file_id: str, content: str) -> bool:
        """
        Index the given corpus and return the index reference.
        
        :param file_id: The ID of the file to index.
        :param content: The content of the document to index.
        :return: True if the document was indexed successfully, False otherwise.
        """
        pass

    @abstractmethod
    async def search(self, query: str) -> list:
        """
        Search for documents in the index.
        
        :param query: The search query.
        :return: A list of document IDs matching the search query.
        """
        pass
