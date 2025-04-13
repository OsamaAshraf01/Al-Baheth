from pydantic import BaseModel, field_validator
from fastapi import UploadFile, HTTPException, File as FastAPIFile, status
from helpers import Annotated
from helpers.config import get_settings
# from models.enums import UnitsEnum

class File(BaseModel):    
    file: Annotated[UploadFile, FastAPIFile(...)]
    @field_validator("file")
    def validate_size(cls, file: UploadFile):
        Settings = get_settings()
        if file.size > (Settings.FILE_MAX_SIZE * 1024 * 1024):
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size is Larger than {Settings.FILE_MAX_SIZE}MB."
            )
        return file
    
    