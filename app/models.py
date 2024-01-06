from pydantic import BaseModel, EmailStr

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
    korisnik_id: str
    ljubimac: str


