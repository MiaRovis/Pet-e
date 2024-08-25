from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from .db import get_database, close_mongo_connection, connect_to_mongo
from .models import Ljubimac, KreiranjeKorisnika, Udomi, DeleteAdoption
from .crud import create_user, get_user, create_pet, get_pets, get_pet, udomi_pet, get_udomi
import logging
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

AsyncIOMotorClientType = AsyncIOMotorClient

@app.get("/")
async def proba():
    return "Okej"

async def startup_event():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    await connect_to_mongo()

async def shutdown_event():
    await close_mongo_connection()

app.add_event_handler("startup", startup_event)
app.add_event_handler("shutdown", shutdown_event)

@app.post("/users/", response_model=str)
async def create_new_user(user: KreiranjeKorisnika, db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        user_id = await create_user(db, user)
        return user_id
    except HTTPException as e:
        logging.warning(f"HTTPException: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=KreiranjeKorisnika)
async def get_user_info(user_id: str, db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        user = await get_user(db, user_id)
        return user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ljubimci/", response_model=str)
async def kreiraj_ljubimca(pet: Ljubimac, db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        pet_id = await create_pet(db, pet)
        return pet_id
    except HTTPException as e:
        logging.warning(f"HTTPException: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ljubimci/", response_model=list[Ljubimac])
async def dohvati_ljubimce(db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        return await get_pets(db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ljubimci/{ljubimac_id}", response_model=Ljubimac)
async def dohvati_ljubimca(ljubimac_id: str, db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        pet = await get_pet(db, ljubimac_id)
        if pet:
            return pet
        raise HTTPException(status_code=404, detail="Pet not found")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/udomi/", response_model=str)
async def udomi_ljubimca(udomi_data: Udomi, db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        result = await udomi_pet(db, udomi_data)
        return result
    except HTTPException as e:
        logging.warning(f"HTTPException: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/udomi/{adoption_id}", response_model=Udomi)
async def get_adoption_request(adoption_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        adoption = await get_udomi(db, adoption_id)
        return adoption
    except HTTPException as e:
        logging.warning(f"HTTPException: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/udomi/{adoption_id}", response_model=DeleteAdoption)
async def delete_adoption_request(adoption_id: str, db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        from bson import ObjectId  
        adoption_request = await db["udomi"].find_one({"_id": ObjectId(adoption_id)})
        if not adoption_request:
            raise HTTPException(status_code=404, detail="Adoption request not found")
        await db["udomi"].delete_one({"_id": ObjectId(adoption_id)})
        return DeleteAdoption(message="Adoption request deleted successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
