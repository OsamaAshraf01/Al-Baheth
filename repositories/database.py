from motor.motor_asyncio import AsyncIOMotorClient
from helpers import Settings
from beanie import init_beanie

async def db_connection(Settings: Settings):
    
    client = AsyncIOMotorClient(Settings.DB_URL)
    await init_beanie(database=client.al_baheth)