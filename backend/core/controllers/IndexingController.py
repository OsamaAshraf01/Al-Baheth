import os

from fastapi import status, Depends
from fastapi.responses import JSONResponse

from .BaseController import BaseController
from .DataController import DataController
from ..services import IndexingService, DirectoryService
from ..models.enums import ResponseEnum
from ..repositories import DocumentRepo


class IndexingController(BaseController):
    def __init__(self,
                 indexing_service: IndexingService,
                 document_repository: DocumentRepo,
                 data_controller: DataController = Depends()):
        super().__init__()
        self.indexing_service = indexing_service
        self.data_controller = data_controller
        self.document_repository = document_repository

    async def index_all(self):
        """
        Index the documents in the assets folder and return the index reference.
        
        :return: JSON response with the index reference.
        """
        corpus = os.listdir(DirectoryService.files_dir)
        index_success_count = 0

        for file_name in corpus:
            content = self.data_controller.parse_file(file_name)
            processed_content = self.data_controller.clean_text(content)

            if await self.document_repository.create(file_name, content, processed_content):
                index_success_count += 1

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": ResponseEnum.INDEXING_SUCCESS.value,
                "total_files": len(corpus),
                "successfully_indexed_files": index_success_count,
                "already_indexed_count": len(corpus) - index_success_count,
            }
        )
