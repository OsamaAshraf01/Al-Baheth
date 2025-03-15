from .BaseController import BaseController
import os
from models.enums import ProcessingEnum
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from helpers import AssertExistence, execution_manager

class ProcessingController(BaseController):
    def get_file_extension(self, file_name):
        return os.path.splitext(file_name)[-1]
    
    def get_file_loader(self, file_name):
        file_extension = self.get_file_extension(file_name)
        file_path = os.path.join(self.files_dir, file_name)

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
        