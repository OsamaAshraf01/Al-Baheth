from fastapi import FastAPI
from routes import base_router, files_router, indexing_router, query_router
from helpers.Lifespan import lifespan

app = FastAPI(lifespan=lifespan)
app.include_router(base_router)
app.include_router(files_router)
app.include_router(query_router)
app.include_router(indexing_router)

