from models import Ljubimac, KreiranjeKorisnika, Korisnik
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from security import get_password_hash
from fastapi import HTTPException

async def create_user(db: AsyncIOMotorClient, user: KreiranjeKorisnika):
    try:
        hashed_password = get_password_hash(user.lozinka)
        user_dict = user.dict()
        user_dict['lozinka'] = hashed_password
        result = await db["users"].insert_one(user_dict)
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def get_user(db: AsyncIOMotorClient, user_id: str):
    try:
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

async def create_pet(db: AsyncIOMotorClient, pet: Ljubimac):
    try:
        result = await db["ljubimci"].insert_one(pet.dict())
        return str(result.inserted_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_pets(db: AsyncIOMotorClient):
    try:
        pets = await db["ljubimci"].find().to_list(length=None)
        return pets
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_pet(db: AsyncIOMotorClient, pet_id: str):
    try:
        pet = await db["ljubimci"].find_one({"_id": ObjectId(pet_id)})
        if pet:
            return pet
        raise HTTPException(status_code=404, detail="Pet not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
