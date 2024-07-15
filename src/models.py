from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, core_schema, handler):
        field_schema = handler(core_schema)
        field_schema.update(type='string')
        return field_schema

class Ljubimac(BaseModel):
    ime: str
    rasa: str
    godiste: int
    opis: str
    status: str

class KreiranjeKorisnika(BaseModel):
    email: EmailStr
    username: str
    lozinka: str

class Korisnik(BaseModel):
    email: EmailStr
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

class Udomi(BaseModel):
    korisnik_id: ObjectId
    ljubimac_id: ObjectId
    datum_udomljavanja: datetime
      
    class Config:
        arbitrary_types_allowed = True


class DeleteAdoption(BaseModel):
    message: str

