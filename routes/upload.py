from fastapi import APIRouter, Depends
from controllers.UploadController import UploadController, UploadFile, File

upload_route = APIRouter(
    prefix= "/upload",
    tags= ["upload"]
)

@upload_route.post("/")
async def upload(file : UploadFile = File(...), controller : UploadController = Depends()):
    return await controller.upload(file)