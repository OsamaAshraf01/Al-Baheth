from fastapi import FastAPI
from contextlib import asynccontextmanager
from repositories import db_connection

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    this function ensures that the database connection is established before the application starts
    and closed when the application shuts down.
    
    :param app: FastAPI application instance.
    """
    await db_connection()
    yield
