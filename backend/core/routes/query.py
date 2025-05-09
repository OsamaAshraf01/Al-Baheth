from fastapi import APIRouter, Depends, status
from starlette.responses import JSONResponse

from ..controllers import QueryController
from ..models.enums import ResponseEnum

query_router = APIRouter(
    prefix="/api/v1/query",
    tags=["api_v1", "query"]
)


@query_router.get("/")
async def query(query: str, controller: QueryController = Depends()):
    results = await controller.query(query)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "summary" : {
                "message": ResponseEnum.SEARCH_SUCCESS.value,
                "query": query,
                "results_count": len(results),
                "results_list": [
                    {
                        f"rank {i}": {
                            "title":doc['title'],
                            "score":doc['score']
                        }
                    }
                    for i, doc in zip(range(1, len(results) + 1), results)
                ]
            },
            "results": results
        }
    )

