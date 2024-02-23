from motor.motor_asyncio import AsyncIOMotorClient

AsyncIOMotorClientType = AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClientType = None

db = DataBase()

def get_database() -> DataBase:
    return db

async def connect_to_mongo():
    db.client = AsyncIOMotorClient("mongodb+srv://admin:<admin>@cluster0.boinvpz.mongodb.net/?retryWrites=true&w=majority")
    db.mongodb = db.client["Pet-e"]

async def close_mongo_connection():
    if db.client:
     db.client.close()