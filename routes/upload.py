from fastapi import APIRouter, Depends
from controllers.UploadController import UploadController, UploadFile, File

upload_router = APIRouter(
    prefix= "/api/v1/upload",
    tags= ["api_v1", "upload"]
)

@upload_router.post("/")
async def upload(file : UploadFile = File(...), controller : UploadController = Depends()):
    return await controller.upload(file)