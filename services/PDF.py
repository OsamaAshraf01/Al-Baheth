from abc import ABC, abstractmethod

class PDFReaderService(ABC):
    """
    Abstract base class for PDF reader services.
    """

    @abstractmethod
    def read(self, file_path: str) -> str:
        """
        Read a PDF file and return its text content.
        
        :param file_path: Path to the PDF file.
        :return: Text content of the PDF file.
        """
        pass
    