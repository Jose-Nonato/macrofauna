from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from bson import ObjectId
from database import db


collection = db['samples']

class MonolithSchema(BaseModel):
    iqms_sample: float = 0.0
    rt: int = 0
    density: float = 0.0
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
    others: Optional[int] = 0

class SampleMonolithsSchema(BaseModel):
    first_monolith: MonolithSchema
    second_monolith: MonolithSchema
    third_monolith: MonolithSchema

class PicturesSchema(BaseModel):
    north: str
    south: str
    east: str
    west: str

class FullSampleSchema(BaseModel):
    id_user: str = Optional
    register_date: datetime = Field(default_factory=datetime.utcnow)
    country: str
    state: str
    city: str
    location: str
    longitude: str
    latitude: str
    iqms: float = 0.0
    rt: int = 0
    sample: SampleMonolithsSchema
    picture: PicturesSchema

    @staticmethod
    def create_sample(data):
        sample = data.model_dump()
        inserted = collection.insert_one(sample)
        return str(inserted.inserted_id)

    @staticmethod
    def get_sample(sample_id: str):
        doc = collection.find_one({'_id': ObjectId(sample_id)})
        return FullSampleSchema(**doc)

    @staticmethod
    def update_sample(sample_id: str, data: dict):
        results = collection.update_one(
            {'_id': ObjectId(sample_id)},
            {'$set': data}
        )
        return results.modified_count > 0

    @staticmethod
    def delete_sample(sample_id: str):
        result = collection.delete_one({'_id': ObjectId(sample_id)})
        return result.deleted_count > 0

    @staticmethod
    def get_sample_active_user(user_id: str):
        data = collection.find(
            {'id_user': user_id},
            {'_id': 1, 'register_date': 1, 'country': 1, 'city': 1, 'state': 1, 'iqms': 1}
        )
        samples = []
        for doc in data:
            if "_id" in doc and isinstance(doc["_id"], ObjectId):
                doc["_id"] = str(doc["_id"])  # 🔑 converte ObjectId -> string
            samples.append(doc)
        return samples
