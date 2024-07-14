from motor.motor_asyncio import AsyncIOMotorClient
import logging
import os
from dotenv import load_dotenv

load_dotenv()

AsyncIOMotorClientType = AsyncIOMotorClient

class DataBase:
    client: AsyncIOMotorClient = None
    mongodb = None

    def __getitem__(self, item):
        if self.mongodb is not None:
            return self.mongodb[item]
        raise ValueError("Database not initialized")

db = DataBase()

async def connect_to_mongo():
    db_url = os.getenv("MONGODB_URL", "mongodb+srv://admin:<admin>@cluster0.boinvpz.mongodb.net/")
    db_name = os.getenv("MONGODB_NAME", "Pet-e")

    if not db_url:
        logging.error("MongoDB URL not found in environment variables")
        raise ValueError("MongoDB URL not found in environment variables")
    try:
        db.client = AsyncIOMotorClient("mongodb+srv://<admin>:<admin>@cluster0.boinvpz.mongodb.net/")
        db.mongodb = db.client[db_name]
        logging.info(f"Connected to MongoDB")
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB")
        raise
    
async def close_mongo_connection():
    if db.client is not None:
        db.client.close()
        logging.info("Closed MongoDB connection")

def get_database() -> DataBase:
    return db
 