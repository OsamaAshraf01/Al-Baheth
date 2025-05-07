import os
from http.client import responses

from aiohttp.abc import HTTPException
from langchain_community.document_loaders import TextLoader, PyMuPDFLoader, Docx2txtLoader, UnstructuredPowerPointLoader
from fastapi import HTTPException, status

from .ParsingService import ParsingService
from ...models.enums import ProcessingEnum, ResponseEnum
from ...services.Directory import DirectoryService


class LangChainService(ParsingService):
    def _get_extension(self, file_name):
        return os.path.splitext(file_name)[-1]

    def _get_file_path(self, file_name) -> str:
        return str(os.path.join(DirectoryService.files_dir, file_name))

    def load(self, file_name):
        file_extension = self._get_extension(file_name)
        file_path = self._get_file_path(file_name)

        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "message": ResponseEnum.FILE_NOT_FOUND.value
                }
            )

        if file_extension == ProcessingEnum.TXT.value:
            return TextLoader(file_path, encoding="utf-8")
        elif file_extension == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(file_path)
        elif file_extension == ProcessingEnum.DOCX.value:
            return Docx2txtLoader(file_path)
        elif file_extension == ProcessingEnum.PPTX.value:
            return UnstructuredPowerPointLoader(file_path)

        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={
                "message": ResponseEnum.FILE_TYPE_NOT_SUPPORTED.value
            }
        )
