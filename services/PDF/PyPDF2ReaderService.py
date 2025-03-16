from services.PDF import PDFReaderService
import PyPDF2

class PyPDF2ReaderService(PDFReaderService):
    """
    Service for reading PDF files using PyPDF2.
    """
    
    def read(self, file_path: str) -> str:
        """
        Read a PDF file and return its text content.
        
        :param file_path: Path to the PDF file.
        :return: Text content of the PDF file.
        """
        text = ""
        
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text()
        
        return text