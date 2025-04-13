from fastapi import APIRouter, Depends
from controllers import IndexingController

indexing_router = APIRouter(
    prefix= "/api/v1/indices",
    tags= ["api_v1", "indexing"]
)

@indexing_router.put('/index_all')
async def index_files(controller: IndexingController = Depends()):
    return controller.index()
