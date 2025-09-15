from datetime import datetime, timedelta
from jose import JWTError, jwt
from models.UserModel import UserModel


SECRET_KEY = '0f9f2dca8809edd5221c5db658a666571e5862fd41dae226712f80e6a29a1455'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthController:
    @staticmethod
    def create_access_token(data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({'exp': expire})
        return jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    

    @staticmethod
    def authenticated_user(email: str, password: str):
        user = UserModel.get_user(email)
        if user and UserModel.verify_password(password, user['hashed_password']):
            return user
        return False
    

    @staticmethod
    def get_current_user(token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
            email: str = payload.get('sub')
            if email is None:
                return None
            user = UserModel.get_user(email)
            return user['_id']
        except JWTError:
            return None
