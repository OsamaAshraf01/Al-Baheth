from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from beanie import init_beanie
from models import Document

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    this function ensures that the database connection is established before the application starts
    and closed when the application shuts down.
    
    :param app: FastAPI application instance.
    """
    db_Settings = get_settings()
    app.client = AsyncIOMotorClient(db_Settings.DB_URL)
    app.db = app.client.al_baheth
    await init_beanie(database=app.db, document_models=[Document])
    
    yield
    
    app.client.close()
