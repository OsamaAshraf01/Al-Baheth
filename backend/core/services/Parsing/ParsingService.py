from abc import ABC, abstractmethod


class ParsingService(ABC):
    """
    Abstract base class for Parsing services.
    """

    @abstractmethod
    def load(self, file_name: str) -> str:
        """
        Read a file and return its text content.
        
        :param file_name: Path to the file.
        :return: Text content of the file.
        """
        pass
