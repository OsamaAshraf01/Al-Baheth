import os

from fastapi import status, Depends
from fastapi.responses import JSONResponse

from .BaseController import BaseController
from .FileController import FileController
from ..services import IndexingService, DirectoryService
from ..models.enums import ResponseEnum


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
        index_success_count = 0

        for doc in corpus:
            file_id = doc['docno']
            content = doc['text']
            if self.indexing_service.index(file_id, content):
                index_success_count += 1

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": ResponseEnum.INDEXING_SUCCESS.value,
                "total_files": len(corpus),
                "successfully_indexed_files": index_success_count,
            }
        )
