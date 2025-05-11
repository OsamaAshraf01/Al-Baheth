from fastapi import APIRouter, Depends, status
import pandas as pd
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

    try:
        qrels = pd.read_csv(r"D:\[01] Projects\[06] Al-Baheth Search Engine\evaluation_data\cisi_rel.csv")
        queries = pd.read_csv(r"D:\[01] Projects\[06] Al-Baheth Search Engine\evaluation_data\cisi_qry.csv")
        query_id = queries[queries['content'].apply(str.strip) == query]['query_id'].values[0]
        relevant_set = set(qrels[qrels['query_id'] == query_id]['doc_id'].astype('str').unique())
        retrieved_docs = [doc['title'].split('.')[0] for doc in results]
        retrieved_set = set(retrieved_docs)

        # Metrics
        precision = len(relevant_set.intersection(retrieved_set)) / len(retrieved_set) if len(retrieved_set) > 0 else None
        recall = len(relevant_set.intersection(retrieved_set)) / len(relevant_set) if len(relevant_set) > 0 else None
        f1_score = 2 * (precision * recall) / (precision + recall) if precision and recall else None
        precision_at_1 = len(relevant_set.intersection(set(retrieved_docs[:1])))
        precision_at_5 = len(relevant_set.intersection(set(retrieved_docs[:5]))) / 5
        precision_at_10 = len(relevant_set.intersection(set(retrieved_docs[:10]))) / 10

        evaluation = {
            "precision": round(precision, 3),
            "recall": round(recall, 3),
            "f1_score": round(f1_score, 3),
            "precision_at_1": round(precision_at_1, 3),
            "precision_at_5": round(precision_at_5, 3),
            "precision_at_10": round(precision_at_10, 3),
        }

    except:
        evaluation = "Not Available"

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "summary" : {
                "message": ResponseEnum.SEARCH_SUCCESS.value,
                "query": query,
                "results_count": len(results),
                "evaluation":evaluation,
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
            "details": results
        }
    )

