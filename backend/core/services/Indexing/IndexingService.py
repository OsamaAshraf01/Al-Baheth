from abc import ABC, abstractmethod

class IndexingService(ABC):
    """
    Abstract base class for indexing services.
    """
    @abstractmethod
    def index(self, corpus: dict) -> str:
        """
        Index the given corpus and return the index reference.
        
        :param corpus: Dictionary containing the corpus to index. It consists of two keys: docno and text.
        :return: Index reference.
        """
        pass