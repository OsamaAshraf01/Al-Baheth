import os, aiofiles, logging

from fastapi import HTTPException, status, Depends, UploadFile

from ..controllers import BaseController
from ..models import File, Document
from ..repositories import DocumentRepo
from ..services import ParsingService, LanguageProcessingService, DirectoryService
from ..models.enums import ResponseEnum
from ..helpers.config import get_settings, Settings
import hashlib

logger = logging.getLogger("uvicorn.error")


class FileController(BaseController):

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


    def parse(self, file_name):
        try:
            loader = self.parsing_service.load(file_name)

            content = loader.load()
            content = "\n".join([doc.page_content for doc in content])

            return content  # the return will be updated to be mor e generic in the future

        except Exception as e:
            raise e


    def paginate(self, text: str, page_size: int = 1000) -> list:
        """
        Paginate the text content.
        
        :param text: Text content to be paginated.
        :param page_size: Tokens count per page.
        :return: List of paginated text content.
        """
        tokens = self.language_processing_service.tokenize(text)
        return [" ".join(tokens[i:i + page_size]) for i in range(0, len(tokens), page_size)]


    def clean(self, text: str) -> str:
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


    def process(self, file_name: str) -> str:
        """
        Processes the content of a specified file by parsing it and 
        cleaning the parsed content.

        This method first retrieves the content of the file using the 
        `parse` method and then applies the `_clean` method to the
        parsed content to prepare it for further processing.

        Args:
            file_name (str): The name of the file to be preprocessed.

        Returns:
            str: The cleaned content of the file as a single string.
        """
        content = self.parse(file_name)
        return self.clean(content)


    async def upload(self, file: File) -> Document:
        """
        Upload a file and process its content.
        
        :param file: File object containing the file information.
        :return: Processed content of the file.
        """
        settings = get_settings()
        file.filename = file.filename.replace(" ", "_").lower()
        file_path = os.path.join(DirectoryService.files_dir, file.filename)

        is_valid, msg = self.validate_uploaded_file(file)

        if not is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "message": msg
                }
            )

        try:
            async with aiofiles.open(file_path, 'wb') as out_file:
                while chunk := await file.read(settings.FILE_DEFAULT_CHUNK_SIZE):
                    await out_file.write(chunk)

        except Exception as e:
            logger.error(f"Error writing file {file.filename}: {str(e)}")

            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

        content = self.process(file_path)
        created_document = await self.document_repository.create(file, content)
        if created_document is None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail={
                    "message": ResponseEnum.FILE_ALREADY_EXISTS.value
                }
            )

        return created_document


    async def query(self, query: str) -> list:
        """
        Search for documents in the index.
        
        :param query: The search query.
        :return: A list of document titles matching the search query.
        """
        query = self.clean(query)
        return await self.document_repository.search(query)


    def validate_uploaded_file(self, file: UploadFile) -> tuple[bool, str]:
        """
        Check if the file is valid.

        :param file: File object to be checked.
        :return: True if the file is valid, False otherwise.
        """

        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseEnum.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * 1024 * 1024:
            return False, ResponseEnum.FILE_SIZE_EXCEEDED.value

        return True, ResponseEnum.FILE_VALID.value
