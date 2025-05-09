from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse

from ..controllers import DataController
from ..models import File
from ..models.enums import ResponseEnum

data_router = APIRouter(
    prefix="/api/v1/data",
    tags=["api_v1", "files", "uploading", "processing"]
)


@data_router.post("/upload")
async def upload(file: File, data_controller: DataController = Depends()):
    # TODO: add a check for the file type and size --[DONE ✓]--
    # TODO: add file processing after upload
    # TODO: add assigning IDs to the files and map them to the main name using simple table
    # TODO: Check if the file hash value already exist to avoid duplicates
    try:
        document = await data_controller.upload_file(file)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "message": ResponseEnum.FILE_UPLOAD_SUCCESS.value,
                "hashed_key": document.hashed_content,
                "title": document.title,
            }
        )
    except HTTPException as e:
        raise e


@data_router.put("/{file_id}/process")
async def process_file(file_id: str, data_controller: DataController = Depends()):
    content = data_controller.parse_file(file_id)
    content = data_controller.clean_text(content)

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": ResponseEnum.PROCESSING_SUCCESS.value,
            "content": content
        }
    )
