from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from ..controllers import FileController
from ..models import File

files_router = APIRouter(
    prefix= "/api/v1/files",
    tags= ["api_v1", "files", "uploading", "processing"]
)

@files_router.post("/upload")
async def upload(file : File, controller : FileController = Depends()):
    #TODO: add a check for the file type and size --[DONE ✓]--
    #TODO: add file processing after upload
    #TODO: add assigning IDs to the files and map them to the main name using simple table
    #TODO: Check if the file hash value already exist to avoid duplicates
    try:
        document = await controller.upload(file)
        
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": "File uploaded successfully",
                "hashed_key": document.hashed_content,
                "content_type": document.content_type,
                "title": document.title,
            }
        )
    except HTTPException as e:
        if e.status_code == status.HTTP_409_CONFLICT:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={
                    "message": f"File {file.filename} already exists!"
                }
            )
        else:
            raise e

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
