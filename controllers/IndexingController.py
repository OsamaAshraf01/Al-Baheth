from fastapi import HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
import os
import pyterrier as pt
from services import IndexingService, DirectoryService
from .BaseController import BaseController
from .ProcessingController import ProcessingController

class IndexingController(BaseController):
    def __init__(self, indexing_service: IndexingService, processing_service: ProcessingController):
        super().__init__()
        self.indexing_service = indexing_service
        self.processing_service = processing_service
    
    
    def process_files(self) -> dict:
        """
        Process files in the assets folder and return a dictionary with docno and their processed text.
        
        :return: Dictionary with docno and text as keys.
        """
        docs = []
        for file_name in os.listdir(DirectoryService.files_dir):
            preprocessed_text = self.processing_service.preprocess(file_name)
            docs.append({
                'docno': file_name,
                'text': preprocessed_text
            })
        
        return docs
    
    def index(self):
        """
        Index the documents in the assets folder and return the index reference.
        
        :return: JSON response with the index reference.
        """
        try:
            corpus = self.process_files()
            index_ref = self.indexing_service.index(corpus)
            return JSONResponse(status_code=status.HTTP_200_OK, content={"index_ref": index_ref})
        except Exception as e:
            return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content={"error": str(e)})
    
    