from .models import Ljubimac, KreiranjeKorisnika, Udomi, Korisnik
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from .utils import get_password_hash
from fastapi import HTTPException
from datetime import datetime
import logging


AsyncIOMotorClientType = AsyncIOMotorClient

async def create_user(db: AsyncIOMotorClientType, user: KreiranjeKorisnika):
    try:
        hashed_password = get_password_hash(user.lozinka)
        user_dict = user.model_dump()
        user_dict['lozinka'] = hashed_password
        result = await db["users"].insert_one(user_dict)
        return str(result.inserted_id)
    except Exception as e:
        logging.error(f"Failed to create user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_user(db: AsyncIOMotorClientType, user_id: str):
    try:
        user = await db["users"].find_one({"_id": ObjectId(user_id)})
        if user:
            return user
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        logging.error(f"Failed to fetch user: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def create_pet(db: AsyncIOMotorClientType, pet: Ljubimac):
    try:
        result = await db["ljubimci"].insert_one(pet.model_dump())
        logging.info(f"Pet created successfully. Pet ID: {str(result.inserted_id)}")
        return str(result.inserted_id)
    except Exception as e:
        logging.error(f"Pet creation failed. Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_pets(db: AsyncIOMotorClientType):
    try:
        pets = await db["ljubimci"].find().to_list(length=None)
        return pets
    except Exception as e:
        logging.error(f"Failed to fetch pets: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_pet(db: AsyncIOMotorClientType, pet_id: str):
    try:
        pet = await db["ljubimci"].find_one({"_id": ObjectId(pet_id)})
        if pet:
            return pet
        raise HTTPException(status_code=404, detail="Pet not found")
    except Exception as e:
        logging.error(f"Failed to fetch pet: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def udomi_pet(db: AsyncIOMotorClientType, udomi_data: Udomi):
    try:
        adoption_data = {
            "korisnik_id": udomi_data.korisnik_id,
            "ljubimac_id": udomi_data.ljubimac_id,
            "datum_udomljavanja": datetime.utcnow()
        }
        result = await db["udomi"].insert_one(adoption_data)
        logging.info(f"Pet adopted successfully. Adopter ID: {udomi_data.korisnik_id}, Pet ID: {udomi_data.ljubimac_id}")
        return str(result.inserted_id)
    except Exception as e:
        logging.error(f"Failed to adopt pet: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
