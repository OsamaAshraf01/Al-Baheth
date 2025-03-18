from fastapi import APIRouter, Depends
from controllers import ProcessingController
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
async def parse(file_name: str, controller : ProcessingController = Depends()):
    return controller.parse(file_name)

@processing_router.get('/preprocess/{file_name}')
async def preprocess(file_name: str, controller : ProcessingController = Depends()):
    return controller.preprocess(file_name)
    
@processing_router.post('/paginate/{file_name}')
async def paginate(file_name: str, controller : ProcessingController = Depends()):
    content = controller.preprocess(file_name)
    pages = controller.paginate(content)
    cleaned = {f"page {i}" : controller._clean(pages[i]) for i in range(len(pages))}
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Message": "Text content cleaned successfully",
            "Processed Text": cleaned
        }
    )