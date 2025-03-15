from fastapi import APIRouter, Depends
from helpers.config import get_settings, Settings
from controllers.ProcessingController import ProcessingController
from fastapi.responses import JSONResponse
from fastapi import status

processing_router = APIRouter(
    prefix='/api/v1/processing',
    tags=["api_v1", "processing"]
)

@processing_router.get('/')
def get_info():
    return JSONResponse(
        status_code=status.HTTP_200_OK, 
        content={
            "message": "Welcome to the processing Endpoint!"
        }
    )

@processing_router.get('/parse/{file_name}')
async def parse(file_name: str):
    controller = ProcessingController()
    content = controller.get_file_content(file_name)
    content = "\n".join([doc.page_content for doc in content])
    return content

@processing_router.get('/preprocess/{file_name}')
async def preprocess(file_name: str):
    controller = ProcessingController()
    content = await parse(file_name)
    
    cleaned = controller._clean(content)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Message": "Text content cleaned successfully",
            "Processed Text": cleaned
        }
    )