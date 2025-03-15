from fastapi import APIRouter, Depends
from controllers.UploadController import uploadController, UploadFile, File

upload_route = APIRouter(
    prefix= "/upload",
    tags= ["upload"]
)

@upload_route.post("/")
async def upload(file : UploadFile = File(...), controller : uploadController = Depends()):
    return await controller.upload(file)