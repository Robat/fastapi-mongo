from motor.motor_asyncio import AsyncIOMotorClient
from app.config.settings import get_settings

db_client = None


async def get_db_client() -> AsyncIOMotorClient:
    global db_client
    settings = get_settings()
    if db_client is None:
        db_client = AsyncIOMotorClient(settings.MONGODB_URL)
    return db_client


async def startup_event():
    global db_client
    db_client = await get_db_client()


async def shutdown_event():
    global db_client
    if db_client:
        db_client.close()
