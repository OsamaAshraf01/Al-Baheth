from fastapi import APIRouter, Depends
from controllers.IndexingController import IndexingController

indexing_router = APIRouter(
    prefix= "/api/v1/indexing",
    tags= ["api_v1", "indexing"]
)

@indexing_router.get('/index')
async def index_files(controller: IndexingController = Depends()):
    return controller.index_all_files()