from fastapi import FastAPI, HTTPException, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from .db import get_database, close_mongo_connection, connect_to_mongo
from .models import Ljubimac, KreiranjeKorisnika, Korisnik, Udomi
from .crud import create_pet, get_pets, get_pet, create_user, get_user, udomi_pet
from .schemas import ErrorResponse
from fastapi import FastAPI, Depends, HTTPException

app = FastAPI()

@app.get("/")
async def proba():
        return "Okej"

@app.on_event("startup")
async def startup_event():
        await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()

@app.post("/users/", response_model=str)
async def create_new_user(user: KreiranjeKorisnika, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        user_id = await create_user(db, user)
        return user_id
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=ErrorResponse(detail=e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(detail=str(e)))

@app.get("/users/{user_id}", response_model=Korisnik)
async def get_user_info(user_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        user = await get_user(db, user_id)
        return user
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=ErrorResponse(detail=e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(detail=str(e)))

@app.post("/ljubimci/", response_model=str)
async def kreiraj_ljubimca(pet: Ljubimac, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        pet_id = await create_pet(db, pet)
        return pet_id
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=ErrorResponse(detail=e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(detail=str(e)))

@app.get("/ljubimci/", response_model=list[Ljubimac])
async def dohvati_ljubimce(db: AsyncIOMotorClient = Depends(get_database)):
    try:
        return await get_pets(db)
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=ErrorResponse(detail=e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(detail=str(e)))

@app.get("/ljubimci/{ljubimac_id}", response_model=Ljubimac)
async def dohvati_ljubimca(ljubimac_id: str, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        pet = await get_pet(db, ljubimac_id)
        if pet:
            return pet
        raise HTTPException(status_code=404, detail="Pet not found")
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=ErrorResponse(detail=e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(detail=str(e)))

@app.post("/udomi/", response_model=str)
async def udomi_ljubimca(udomi_data: Udomi, db: AsyncIOMotorClient = Depends(get_database)):
    try:
        result = await udomi_pet(db, udomi_data)
        return result
    except HTTPException as e:
        raise HTTPException(status_code=e.status_code, detail=ErrorResponse(detail=e.detail))
    except Exception as e:
        raise HTTPException(status_code=500, detail=ErrorResponse(detail=str(e)))