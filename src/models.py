from pydantic import BaseModel, EmailStr, validator
from bson import ObjectId
from datetime import datetime

class Ljubimac(BaseModel):
    ime: str
    rasa: str
    godiste: int
    opis: str
    status: str

class KreiranjeKorisnika(BaseModel):
    email: EmailStr
    lozinka: str

class Korisnik(BaseModel):
    email: EmailStr
    id: str

class Udomi(BaseModel):
    korisnik_id: ObjectId
    ljubimac_id: ObjectId
    datum_udomljavanja: datetime


class DeleteAdoption(BaseModel):
    message: str

