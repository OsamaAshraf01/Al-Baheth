from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import Settings, get_settings
from fastapi import Depends
from beanie import init_beanie

async def db_connection():
    db_Settings: Settings = get_settings()
    client = AsyncIOMotorClient(db_Settings.DB_URL)
    await init_beanie(database=client.al_baheth)