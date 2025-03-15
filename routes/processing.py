from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings
from controllers.ProcessingController import ProcessingController

processing_router = APIRouter(
    prefix='/api/v1/process',
    tags=["api_v1", "processing"]
)

@processing_router.get('/')
def get_info():
    return {
        "message": "Welcome to the processing Endpoint!"
    }

@processing_router.get('/parse/{file_name}')
async def parse(file_name: str, controller: ProcessingController = Depends()):
    return await controller.parse(file_name)