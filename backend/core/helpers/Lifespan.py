from contextlib import asynccontextmanager

from beanie import init_beanie
from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from sentence_transformers import SentenceTransformer
import torch

from ..helpers.config import get_settings
from ..models import Document
from ..models.enums import IndexingEnum


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    this function ensures that the database connection is established before the application starts
    and closed when the application shuts down.
    
    :param app: FastAPI application instance.
    """
    _settings_ = get_settings()

    # database connection
    app.mongodb_client = AsyncIOMotorClient(_settings_.DB_URL)
    app.db = app.mongodb_client.al_baheth
    await init_beanie(database=app.db, document_models=[Document])

    # initialize the embedding model
    app.embedding_model = SentenceTransformer(_settings_.EMBEDDING_MODEL)
    embedding_device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    app.embedding_model = app.embedding_model.to(embedding_device)

    if _settings_.INDEXING_SERVICE == IndexingEnum.ElasticSearch.value:
        app.es_client = AsyncElasticsearch(_settings_.ES_URL)
        if not await app.es_client.indices.exists(index=_settings_.ES_INDEXING):
            await app.es_client.indices.create(
                index=_settings_.ES_INDEXING,
                mappings={
                    "properties": {
                        "file_id" : {
                            "type": "text"
                        },
                        "embedding": {
                            "type": "dense_vector",
                            "similarity": "cosine",
                            "dims": 768,
                            "index": True
                        }
                    }
                }
            )

    yield

    app.mongodb_client.close()

    if _settings_.INDEXING_SERVICE == IndexingEnum.ElasticSearch.value:
        await app.es_client.close()
