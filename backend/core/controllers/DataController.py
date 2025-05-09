import os, aiofiles, logging

from fastapi import HTTPException, status
from fastapi.params import Depends

from ..controllers import BaseController
from ..models import File, Document
from ..repositories import DocumentRepo
from ..services import ParsingService, LanguageProcessingService, DirectoryService
from ..models.enums import ResponseEnum
from ..helpers.config import get_settings, Settings

logger = logging.getLogger("uvicorn.error")


class DataController(BaseController):

    def __init__(
            self,
            parsing_service: ParsingService,
            language_processing_service: LanguageProcessingService,
            document_repository: DocumentRepo
    ):

        super().__init__()
        self.parsing_service = parsing_service
        self.language_processing_service = language_processing_service
        self.document_repository = document_repository


    def parse_file(self, file_name):
        try:
            loader = self.parsing_service.load(file_name)

            content = loader.load()
            content = "\n".join([doc.page_content for doc in content])

            return content  # the return will be updated to be mor e generic in the future

        except Exception as e:
            raise e


    def clean_text(self, text: str) -> str:
        """
        Clean the extracted text.
        
        :param text: Extracted text from a file.
        :return: Cleaned text.
        """

        # Normalization
        text = self.language_processing_service.normalize(text)

        # Tokenization
        tokens = self.language_processing_service.tokenize(text)

        # Stopwords removal
        tokens = self.language_processing_service.remove_stopwords(tokens)

        processed_tokens = self.language_processing_service.lemmatize(tokens)

        # Stemming
        processed_tokens = self.language_processing_service.stem(processed_tokens)

        return ' '.join(processed_tokens)


    async def upload_file(self, file: File, settings: Settings = Depends(get_settings)) -> Document:
        """
        Upload a file and process its content.
        
        :param file: File object containing the file information.
        :param settings: Settings object containing application settings.
        :return: Processed content of the file.
        """
        file.filename = file.filename.replace(" ", "_").lower()
        file_path = os.path.join(DirectoryService.files_dir, file.filename)

        try:
            async with aiofiles.open(file_path, 'wb') as out_file:
                while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                    await out_file.write(chunk)

        except Exception as e:
            logger.error(f"Error writing file {file.filename}: {str(e)}")

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content = self.parse_file(file_path)
        processed_content = self.clean_text(content)
        created_document = await self.document_repository.create(file.filename, content, processed_content)
        if created_document is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": ResponseEnum.FILE_ALREADY_EXISTS.value
                }
            )

        return created_document
