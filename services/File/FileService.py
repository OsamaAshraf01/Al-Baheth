from abc import ABC, abstractmethod

class FileService(ABC):
    """
    Abstract base class for reading files.

    This class defines an interface for reading files. Any subclass must implement
    the `load` method to provide specific file reading functionality.
    """

    @abstractmethod
    def load(self, file_name: str):
        """
        Reads the contents of a file.

        Args:
            file_name (str): The name of the file to read.

        Returns:
            str: The contents of the file as a string.
        """
        pass