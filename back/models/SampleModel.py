from pydantic import BaseModel
from database import db


collection = db['sample']

class InsectSchema(BaseModel):
    earthworm: int
    ant: int
    isoptera: int
    blattaria: int
    coleoptera: int
    arachnida: int
    diplopoda: int
    chilopoda: int
    hemiptera: int
    gasteropida: int
    others: int


class PicturesSchema(BaseModel):
    north: str
    south: str
    east: str
    west: str


class SampleSchema(BaseModel):
    user_id: str
    register_date: str
    longitude: str
    latitude: str
    country: str
    state: str
    city: str
    density: float
    iqms: float
    insect: InsectSchema
    picture: PicturesSchema


    @staticmethod
    def create_sample(data: dict):
        results = collection.insert_one(data)
        return str(results.inserted_id)


    @staticmethod
    def get_sample(sample_id: str):
        env = collection.find_one({'_id': sample_id})
        if env:
            return env
        return None
