from pydantic import BaseModel, field_validator
from fastapi import UploadFile, HTTPException, File as FastAPIFile, status
from helpers import Settings

class File(BaseModel):
    file: UploadFile = FastAPIFile(...)
    
    @field_validator("file")
    def validate_size(cls, file: UploadFile, Settings: Settings):
        if file.size > Settings.FILE_MAX_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail=f"File size is Larger than {Settings.FILE_MAX_SIZE / (1024 * 1024)}MB."
            )
        return file
    
    