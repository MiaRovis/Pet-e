from pydantic import BaseModel, EmailStr, Field
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

class Udomi(BaseModel):
    korisnik_id: ObjectId
    ljubimac_id: ObjectId
    datum_udomljavanja: datetime
      
    class Config:
        arbitrary_types_allowed = True


class DeleteAdoption(BaseModel):
    message: str

