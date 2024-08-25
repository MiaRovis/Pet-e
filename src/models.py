from pydantic import BaseModel, EmailStr
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
    korisnik: str
    ljubimac: str
    datum_udomljavanja: datetime

class DeleteAdoption(BaseModel):
    message: str

