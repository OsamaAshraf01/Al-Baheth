from fastapi import UploadFile, HTTPException, File as FastAPIFile, Depends, status

from ..helpers import Annotated
from ..helpers.config import get_settings
from ..models.enums import ResponseEnum


class _File:
    """A dependency class that checks file size"""

    def __init__(self):
        settings = get_settings()
        self.max_size = settings.FILE_MAX_SIZE
        self.allowed_types = settings.FILE_ALLOWED_TYPES

    async def __call__(self, file: UploadFile = FastAPIFile(...)) -> UploadFile:
        if file.size > self.max_size * 1024 * 1024:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=ResponseEnum.FILE_SIZE_EXCEEDED.value
            )

        if file.content_type not in self.allowed_types:
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=ResponseEnum.FILE_TYPE_NOT_SUPPORTED.value
            )

        return file


File = Annotated[UploadFile, Depends(_File())]
