from abc import ABC, abstractmethod

class IndexingService(ABC):
    """
    Abstract base class for indexing services.
    """
    @abstractmethod
    async def index(self, file_id: str, content: str) -> bool:
        """
        Index the given corpus and return the index reference.
        
        :param corpus: Dictionary containing the corpus to index. It consists of two keys: docno and text.
        :return: Index reference.
        """
        pass
    
    async def search(self, query: str) -> list:
        """
        Search for documents in the index.
        
        :param query: The search query.
        :return: A list of documents IDs matching the search query.
        """
        pass