import os

from fastapi import status, Depends
from fastapi.responses import JSONResponse

from .BaseController import BaseController
from .FileController import FileController
from ..services import IndexingService, DirectoryService


class IndexingController(BaseController):
    def __init__(self, indexing_service: IndexingService, processing_controller: FileController = Depends()):
        super().__init__()
        self.indexing_service = indexing_service
        self.processing_controller = processing_controller

    def process_files(self) -> dict:
        """
        Process files in the assets folder and return a dictionary with docno and their processed text.
        
        :return: Dictionary with docno and text as keys.
        """
        docs = []
        for file_name in os.listdir(DirectoryService.files_dir):
            preprocessed_text = self.processing_controller.process(file_name)
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
        corpus = self.process_files()
        index_ref = self.indexing_service.index(corpus)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Indexing completed successfully",
                # "index_ref": index_ref
            }
        )
