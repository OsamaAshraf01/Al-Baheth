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
async def parse(file_name: str):
    controller = ProcessingController()
    content = controller.get_file_content(file_name)
    content = "\n".join([doc.page_content for doc in content])
    return content

@processing_router.get('/preprocess/{file_name}')
async def preprocess(file_name: str, controller : ProcessingController = Depends()):
    content = await parse(file_name)
    return controller._clean(content)
    
@processing_router.post('/paginate/{file_name}')
async def paginate(file_name: str):
    content = await preprocess(file_name)
    controller = ProcessingController()
    pages = controller.paginate(content)
    cleaned = {f"page {i}" : controller._clean(pages[i]) for i in range(len(pages))}
    
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "Message": "Text content cleaned successfully",
            "Processed Text": cleaned
        }
    )