from controllers import BaseController
from helpers import execution_manager
from services import PDFReaderService, LanguageProcessingService, FileService
from fastapi import HTTPException, status


class ProcessingController(BaseController):
    
    def __init__(
        self, 
        PDFReaderService: PDFReaderService, 
        LanguageProcessingService: LanguageProcessingService,
        FileService: FileService
        
        ):
        
        super().__init__()
        self.PDFReaderService = PDFReaderService
        self.LanguageProcessingService = LanguageProcessingService
        self.FileService = FileService

    @execution_manager
    def load(self, file_name):
        loader= self.FileService.load(file_name)
        
        if loader is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": f"File {file_name} not found!"
                }
            )
        
        return loader.load()  # the return will be updated to be mor e generic in the future
    
    def paginate(self, text: str, page_size: int = 1000) -> list:
        """
        Paginate the text content.
        
        :param text: Text content to be paginated.
        :param page_size: Tokens count per page.
        :return: List of paginated text content.
        """
        tokens = self.LanguageProcessingService.tokenize(text)
        return [" ".join(tokens[i:i + page_size]) for i in range(0, len(tokens), page_size)] 
    
    def _read(self, file_name: str) -> str:
        """
        Read the PDF file and extract text content.
        
        :param: file_path: Path to the PDF file.
        :return: Text content of the PDF file.
        """
        file_path = self._get_file_path(file_name)
        text = self.PDFReaderService.read(file_path)
        return text
    
    def _clean(self, text: str) -> str:
        """
        Clean the extracted text.
        
        :param text: Extracted text from the PDF.
        :return: Cleaned text.
        """

        # Normalization
        text = self.LanguageProcessingService.normalize(text)

        # Tokenization
        tokens = self.LanguageProcessingService.tokenize(text)

        # Stopwords removal
        tokens = self.LanguageProcessingService.remove_stopwords(tokens)

        processed_tokens = self.LanguageProcessingService.lemmatize(tokens)  
        
        # Stemming
        processed_tokens = self.LanguageProcessingService.stem(processed_tokens)

        return ' '.join(processed_tokens)
    
    def parse(self, file_name: str) -> str:
        """
        Parses the content of a file and returns it as a single string.

        This method retrieves the content of the specified file, extracts the 
        page content from each document, and joins them into a single string 
        separated by newline characters.

        Args:
            file_name (str): The name of the file to be parsed.

        Returns:
            str: The combined content of the file as a single string.
        """
        content = self.load(file_name)
        content = "\n".join([doc.page_content for doc in content])
        return content
    
    def preprocess(self, file_name: str) -> str:
        """
        Preprocesses the content of a specified file by parsing it and 
        cleaning the parsed content.

        This method first retrieves the content of the file using the 
        `parse` method, and then applies the `_clean` method to the 
        parsed content to prepare it for further processing.

        Args:
            file_name (str): The name of the file to be preprocessed.

        Returns:
            str: The cleaned content of the file as a single string.
        """
        content = self.parse(file_name)
        return self._clean(content)