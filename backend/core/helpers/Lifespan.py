from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from ..helpers.config import get_settings
from beanie import init_beanie
from ..models import Document
from ..models.enums import IndexingEnum
from elasticsearch import AsyncElasticsearch

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    this function ensures that the database connection is established before the application starts
    and closed when the application shuts down.
    
    :param app: FastAPI application instance.
    """
    _settings_ = get_settings()
    app.mongodb_client = AsyncIOMotorClient(_settings_.DB_URL)
    app.db = app.mongodb_client.al_baheth
    await init_beanie(database=app.db, document_models=[Document])
    
    if _settings_.INDEXING_SERVICE == IndexingEnum.ElasticSearch.value:
        app.es_client = AsyncElasticsearch(_settings_.ES_URL)
        if not await app.es_client.indices.exists(index=_settings_.ES_INDEXING):
            await app.es_client.indices.create(
                index=_settings_.ES_INDEXING,
                mappings={
                    "properties": {
                        "file_id": {"type": "keyword"},
                        "content": {"type": "text"}
                    }
                }
            )

    yield
    
    app.mongodb_client.close()
    
    if _settings_.INDEXING_SERVICE == IndexingEnum.ElasticSearch.value:
        await app.es_client.close()
