from controllers import BaseController
from fastapi import Depends
import os
from models.enums import ProcessingEnum
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from helpers import execution_manager
from dependencies import getPDFReaderService, getLanguageService
from services import PDFReaderService, LanguageService
from fastapi.responses import JSONResponse
from fastapi import status


class ProcessingController(BaseController):
    
    def __init__(
        self, 
        PDFReaderService: PDFReaderService = Depends(getPDFReaderService), 
        LanguageService: LanguageService = Depends(getLanguageService)
        ):
        
        super().__init__()
        self.PDFReaderService = PDFReaderService
        self.LanguageService = LanguageService
    
    def get_file_extension(self, file_name):
        return os.path.splitext(file_name)[-1]
    
    def _get_file_path(self, file_name):
        return os.path.join(self.files_dir, file_name)
    
    def get_file_loader(self, file_name):
        file_extension = self.get_file_extension(file_name)
        file_path = self._get_file_path(file_name)

        if not os.path.exists(file_path):
            return None
        
        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_extension == ProcessingEnum.DOCX.value:
            return Docx2txtLoader(file_path)
        elif file_extension == ProcessingEnum.PPTX.value:
            return UnstructuredPowerPointLoader(file_path)
        
        return None
    

    @execution_manager
    def get_file_content(self, file_name):
        loader = self.get_file_loader(file_name)
        
        if loader is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={
                    "message": f"File {file_name} not found!"
                }
            )
        
        return loader.load()
    
    def paginate(self, text: str, page_size: int = 1000) -> list:
        """
        Paginate the text content.
        
        :param text: Text content to be paginated.
        :param page_size: Tokens count per page.
        :return: List of paginated text content.
        """
        tokens = self.LanguageService.tokenize(text)
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
        text = self.LanguageService.normalize(text)

        # Tokenization
        tokens = self.LanguageService.tokenize(text)

        # Stopwords removal
        tokens = self.LanguageService.remove_stopwords(tokens)

        processed_tokens = self.LanguageService.lemmatize(tokens)  
        
        # Stemming
        processed_tokens = self.LanguageService.stem(processed_tokens)

        return ' '.join(processed_tokens)
    
    def preprocess(self, file_name: str) -> str:
        """
        Preprocess the PDF file and return its cleaned text content.
        
        :param file_name: Path to the PDF file.
        :return: Cleaned text content of the PDF file.
        """
        try:
            text = self._read(file_name)
        except:
            raise Exception("Error reading the PDF file.")
        
        try:
            text = self._clean(text)
        except: 
            raise Exception("Error cleaning the text.")
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": f"Text of file {file_name} has been preprocessed successfully!", 
            }
        )
    