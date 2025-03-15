from .BaseController import BaseController
from fastapi import Depends
import os, re
from models.enums import ProcessingEnum
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from helpers import AssertExistence, execution_manager
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from dependencies import getPDFReaderService
from services.PDF import PDFReaderService


class ProcessingController(BaseController):
    
    def __init__(self, PDFReaderService: PDFReaderService = Depends(getPDFReaderService)):
        self.PDFReaderService = PDFReaderService
    
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
        
        AssertExistence(loader)
        
        return loader.load()
    
    def _read(self, file_name: str) -> str:
        """
        Read the PDF file and extract text content.
        
        :param: file_path: Path to the PDF file.
        :return: Text content of the PDF file.
        """
        file_path = self._get_file_path(file_name)
        text = self.PDFReaderService.read(file_path)
        return text
    
    def _clean(self, text: str, stemmer = Depends(PorterStemmer)) -> str:
        """
        Clean the extracted text.
        
        :param text: Extracted text from the PDF.
        :return: Cleaned text.
        """

        tokens = word_tokenize(text)

        text = text.lower()
        text = re.sub("[^a-z ]+", " ", text).strip()

        stop_words = set(stopwords.words('english'))
        processed_tokens = [stemmer.stem(word) for word in tokens if word not in stop_words]

        return ' '.join(processed_tokens)
    
    def preprocess(self, file_name: str) -> str:
        """
        Preprocess the PDF file and return its cleaned text content.
        
        :param file_name: Path to the PDF file.
        :return: Cleaned text content of the PDF file.
        """
        try:
            text = self._read(file_name)
        except: raise Exception("Error reading the PDF file.")
        
        try:
            text = self._clean(text)
        except: raise Exception("Error cleaning the text.")
        return "claened text"