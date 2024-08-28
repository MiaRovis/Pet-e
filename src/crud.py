from .models import Ljubimac, KreiranjeKorisnika, Udomi
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
    
async def get_all_users(db: AsyncIOMotorClientType):
    try:
        users = await db["users"].find().to_list(length=None) 
        return users
    except Exception as e:
        logging.error(f"Failed to fetch users: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch users")

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
            "korisnik": udomi_data.korisnik,
            "ljubimac": udomi_data.ljubimac,
            "datum_udomljavanja": datetime.utcnow()
        }
        result = await db["udomi"].insert_one(adoption_data)
        logging.info(f"Pet adopted successfully. Adopter: {udomi_data.korisnik}, Pet: {udomi_data.ljubimac}")
        return str(result.inserted_id)
    except Exception as e:
        logging.error(f"Failed to adopt pet: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_all_udomi(db: AsyncIOMotorClientType):
    try:
        adoption_requests = await db["udomi"].find().to_list(length=None)
        return adoption_requests
    except Exception as e:
        logging.error(f"Failed to fetch adoption requests: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch adoption requests")
    
async def get_udomi(db: AsyncIOMotorClient, adoption_id: str):
    try:
        adoption = await db["udomi"].find_one({"_id": ObjectId(adoption_id)})
        if not adoption:
            raise HTTPException(status_code=404, detail="Adoption request not found")
        return adoption
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_adoption_request(db: AsyncIOMotorClientType, adoption_id: str):
    try:
        adoption_request = await db["udomi"].find_one({"_id": ObjectId(adoption_id)})
        if not adoption_request:
            raise HTTPException(status_code=404, detail="Adoption request not found")

        result = await db["udomi"].delete_one({"_id": ObjectId(adoption_id)})
        
        if result.deleted_count == 0:
            raise HTTPException(status_code=404, detail="Failed to delete adoption request")

        logging.info(f"Adoption request deleted successfully. Adoption ID: {adoption_id}")
        return {"message": "Adoption request deleted successfully"}
    
    except Exception as e:
        logging.error(f"Failed to delete adoption request. Error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete adoption request")