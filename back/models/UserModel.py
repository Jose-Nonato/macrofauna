from pydantic import BaseModel, EmailStr
from typing import Optional
from bson import ObjectId
from database import db
from passlib.hash import bcrypt

collection = db["users"]


class UserModel(BaseModel):
    email: EmailStr
    hashed_password: str
    is_active: Optional[bool] = True


    @staticmethod
    def get_user(email: str):
        user = collection.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
            return user
        return None
    

    @staticmethod
    def create_user(user_data):
        result = collection.insert_one(user_data)
        return result.inserted_id
    

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return bcrypt.verify(plain_password, hashed_password)
    

    @staticmethod
    def hash_password(password):
        return bcrypt.hash(password)
