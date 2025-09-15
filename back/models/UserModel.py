from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from bson import ObjectId
from database import db
from passlib.hash import bcrypt

collection = db["users"]


class UserExtrasUpdate(BaseModel):
    name: Optional[str] = None
    profission: Optional[str] = None
    training: Optional[str] = None
    university: Optional[str] = None
    birth_date: Optional[str] = None


class UserModel(BaseModel):
    name: Optional[str] = None
    email: EmailStr
    hashed_password: str
    profission: Optional[str] = None
    training: Optional[str] = None
    university: Optional[str] = None
    birth_date: Optional[str] = None
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


    @staticmethod
    def update_user(user_id: str, update_data: Dict[str, Any]):
        if not ObjectId.is_valid(user_id):
            return None
        update_data.pop("email", None)
        update_data.pop("password", None)
        update_data.pop("hashed_password", None)
        update_data.pop("is_active", None)

        update_data = {k: v for k, v in update_data.items() if v is not None}
        if not update_data:
            return None
        
        result = collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": update_data}
        )
        if result.matched_count == 0:
            return None
        
        user = collection.find_one({"_id": ObjectId(user_id)})
        user["_id"] = str(user["_id"])
        return user
