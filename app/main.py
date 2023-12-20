from fastapi import FastAPI
from .db import connect_to_mongo, close_mongo_connection

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



