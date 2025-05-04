from fastapi import UploadFile, HTTPException, File as FastAPIFile, Depends
from ..helpers import Annotated
from ..helpers.config import get_settings
# from models.enums import UnitsEnum

class _File:
    """A dependency class that checks file size"""
    def __init__(self):
        settings = get_settings()
        self.max_size = settings.FILE_MAX_SIZE
    
    async def __call__(self, file: UploadFile = FastAPIFile(...)) -> UploadFile:
        
        if file.size > self.max_size * 1024 * 1024:
            raise HTTPException(
                status_code=413,
                detail=f"File too large. Maximum size allowed is {self.max_size} MB"
            )
            
        return file
    
File = Annotated[UploadFile, Depends(_File())]