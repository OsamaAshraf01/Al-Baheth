from fastapi import FastAPI, File, UploadFile, HTTPException
import os
from .BaseController import BaseController

class UploadController(BaseController):
    
    async def upload(self, file: UploadFile = File(...)):
        file_path = os.path.join(self.files_dir, file.filename)
        try:
            with open(file_path, "wb") as f:
                f.write(await file.read())
        except:
            raise HTTPException(status_code=400, detail="Failed to upload the file")
        
        return {"Message": "Successfully uploaded"}