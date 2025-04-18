from controllers import BaseController
from services import ParsingService, LanguageProcessingService
from fastapi import HTTPException, status


class ProcessingController(BaseController):
    
    def __init__(
            self, 
            ParsingService: ParsingService, 
            LanguageProcessingService: LanguageProcessingService,
        ):
        
        super().__init__()
        self.ParsingService = ParsingService
        self.LanguageProcessingService = LanguageProcessingService

    def parse(self, file_name):
        loader= self.ParsingService.load(file_name)
        
        if loader is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": f"File {file_name} not found!"
                }
            )
            
        content = loader.load()
        content = "\n".join([doc.page_content for doc in content])
        
        return content  # the return will be updated to be mor e generic in the future
    
    def paginate(self, text: str, page_size: int = 1000) -> list:
        """
        Paginate the text content.
        
        :param text: Text content to be paginated.
        :param page_size: Tokens count per page.
        :return: List of paginated text content.
        """
        tokens = self.LanguageProcessingService.tokenize(text)
        return [" ".join(tokens[i:i + page_size]) for i in range(0, len(tokens), page_size)] 
    
    
    def _clean(self, text: str) -> str:
        """
        Clean the extracted text.
        
        :param text: Extracted text from a file.
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
    
    
    def process(self, file_name: str) -> str:
        """
        Processes the content of a specified file by parsing it and 
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