from models import File
import os
from .BaseController import BaseController
from fastapi.responses import JSONResponse
from fastapi import status
from services import DirectoryService

class UploadController(BaseController):
    def __init__(self):
        super().__init__()
    async def upload(self, file: File):
        file_path = os.path.join(DirectoryService.files_dir, file.file.filename)
        try:
            with open(file_path, "wb") as f:
                f.write(await file.file.read())
        except:
            raise JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST, 
                content={
                    "Message" : "Failed to upload the file"
                }
            )
        
        return JSONResponse(
            status_code=200,
            content={
                "Message": "Successfully uploaded"
            }
        )