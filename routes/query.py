from fastapi import APIRouter
from controllers import QueryController

query_router = APIRouter(
    prefix= "/api/v1/query",
    tags= ["api_v1", "query"]
)

@query_router.get("/")
async def query(query : str):
    controller = QueryController()
    return await controller.query(query)