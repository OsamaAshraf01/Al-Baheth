from .ParsingService import ParsingService
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from models.enums import ProcessingEnum
from services.Directory import DirectoryService
import os
class LangChainService(ParsingService):
    def _get_extension(self, file_name):
        return os.path.splitext(file_name)[-1]
    
    def _get_file_path(self, file_name):
        return os.path.join(DirectoryService.files_dir, file_name)
    
    def load(self, file_name):
        file_extension = self._get_extension(file_name)
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