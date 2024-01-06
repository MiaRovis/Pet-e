from models import Ljubimac, KreiranjeKorisnika, Korisnik
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

async def create_user(db: AsyncIOMotorClient, user: KreiranjeKorisnika):
    result = await db["users"].insert_one(user.dict())
    return str(result.inserted_id)

async def get_user(db: AsyncIOMotorClient, user_id: str):
    user = await db["users"].find_one({"_id": ObjectId(user_id)})
    return user

async def create_pet(db: AsyncIOMotorClient, pet: Ljubimac):
    result = await db["ljubimci"].insert_one(pet.dict())
    return str(result.inserted_id)

async def get_pets(db: AsyncIOMotorClient):
    pets = await db["ljubimci"].find().to_list(length=None)
    return pets

async def get_pet(db: AsyncIOMotorClient, pet_id: str):
    pet = await db["ljubimci"].find_one({"_id": ObjectId(pet_id)})
    return pet
