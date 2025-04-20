from fastapi import APIRouter, Depends, UploadFile, File as FastapiFile, status
from fastapi.responses import JSONResponse
from controllers import UploadController, FileController
from models import File

files_router = APIRouter(
    prefix= "/api/v1/files",
    tags= ["api_v1", "files", "uploading", "processing"]
)

@files_router.post("/upload")
async def upload(file : UploadFile = FastapiFile(...), controller : UploadController = Depends()):
    #TODO: add a check for the file type and size --[DONE ✓]--
    #TODO: add file processing after upload
    #TODO: add assigning IDs to the files and map them to the main name using simple table
    #TODO: Check if the file hash value already exist to avoid duplicates
    return await controller.upload(File(file=file))

@files_router.put("/{file_id}/process")
async def process_file(file_id: str, controller: FileController = Depends()):
    content = controller.process(file_id)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "File processed successfully",
            "content": content
        }
    )
