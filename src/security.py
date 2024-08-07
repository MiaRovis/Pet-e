from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from .db import get_database, close_mongo_connection, connect_to_mongo
from .models import KreiranjeKorisnika, Korisnik, Ljubimac, Udomi, DeleteAdoption, PyObjectId
import logging
from dotenv import load_dotenv
from bson import ObjectId
from .utils import get_password_hash

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
    from .crud import create_user
    try:
        user_id = await create_user(db, user)
        logging.info(f"User created successfully. User ID: {user_id}")
        return user_id
    except HTTPException as e:
        logging.warning(f"HTTPException: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}", response_model=Korisnik)
async def get_user_info(user_id: PyObjectId, db: AsyncIOMotorClientType = Depends(get_database)):
    from .crud import get_user
    try:
        user = await get_user(db, user_id)
        return user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ljubimci/", response_model=str)
async def kreiraj_ljubimca(pet: Ljubimac, db: AsyncIOMotorClientType = Depends(get_database)):
    from .crud import create_pet 
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
    from .crud import get_pets
    try:
        return await get_pets(db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/ljubimci/{ljubimac_id}", response_model=Ljubimac)
async def dohvati_ljubimca(ljubimac_id: str, db: AsyncIOMotorClientType = Depends(get_database)):
    from .crud import get_pet 
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
    from .crud import udomi_pet
    try:
        result = await udomi_pet(db, udomi_data)
        return result
    except HTTPException as e:
        logging.warning(f"HTTPException: {e}")
        raise HTTPException(status_code=e.status_code, detail=str(e.detail))
    except Exception as e:
        logging.error(f"An error occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/udomi/{adoption_id}", response_model=DeleteAdoption)
async def delete_adoption_request(adoption_id: str, db: AsyncIOMotorClientType = Depends(get_database)):
    try:
        adoption_request = await db["udomi"].find_one({"_id": ObjectId(adoption_id)})
        if not adoption_request:
            raise HTTPException(status_code=404, detail="Adoption request not found")
        await db["udomi"].delete_one({"_id": ObjectId(adoption_id)})
        return DeleteAdoption(message="Adoption request deleted successfully")
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
