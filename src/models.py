from pydantic import BaseModel, EmailStr
from datetime import datetime

# Model koji deifinira ljubimca, navedene su vrijednosti ime, rada, godiste
# opis te status -> potrebno za kreiranje ljubimaca

class Ljubimac(BaseModel):
    ime: str
    rasa: str
    godiste: int
    opis: str
    status: str

# Model koji definira korisnika, za kreiranje korisnika potreban je 
# email te lozinka

class KreiranjeKorisnika(BaseModel):
    email: EmailStr
    lozinka: str

# Model koji definira zahtjev za udomljenje, nakon kreiranog korisnika i 
# ljubimca, možemo kreirati zahtjev za udomljenje

class Udomi(BaseModel):
    korisnik: str
    ljubimac: str
    datum_udomljavanja: datetime

# Model koji definira brisanje zahtjeva za udomljenje

class DeleteAdoption(BaseModel):
    message: str

