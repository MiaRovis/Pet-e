from pydantic import BaseModel, EmailStr

class Ljubimac(BaseModel):
    ime: str
    rasa: str
    godiste: int
    opis: str
    status: str

class Korisnik(BaseModel):
    email: EmailStr
    id: str

class Udomi(BaseModel):
    korisnik_id: str
    ljubimac: str


