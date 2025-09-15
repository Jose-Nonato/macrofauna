from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from controller.AuthController import AuthController
from models.UserModel import UserModel, UserExtras

router = APIRouter()
oauth2scheme = OAuth2PasswordBearer(tokenUrl='token')


@router.post('/register')
async def register_user(form_data: OAuth2PasswordRequestForm = Depends()):
    existing_user = UserModel.get_user(form_data.username)
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')
    hashed_password = UserModel.hash_password(form_data.password)
    user_data = {'email': form_data.username, 'hashed_password': hashed_password, 'isActive': True}
    UserModel.create_user(user_data)
    return {'msg': 'User created successfully'}


@router.post('/token')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = AuthController.authenticated_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    access_token = AuthController.create_access_token(data={'sub': user['email']})
    return {'access_token': access_token, 'token_type': 'bearer'}


@router.get('/users/extras')
def user_extras(token: str = Depends(oauth2scheme)):
    current_user = AuthController.get_current_user(token)

    if current_user is None:
        raise HTTPException(status_code=401, detail='Invalid token')
    
    user_info = UserModel.get_user_info(current_user)

    if not user_info:
        return HTTPException(status_code=404, detail='User not found or no valid data submitted')
    
    return user_info


@router.put('/users/extras')
def update_user_extras(user_update: UserExtras, token: str = Depends(oauth2scheme)):
    current_user = AuthController.get_current_user(token)

    if current_user is None:
        raise HTTPException(status_code=401, detail='Invalid token')

    updated_users = UserModel.update_user(current_user, user_update.dict(exclude_unset=True))

    if not updated_users:
        raise HTTPException(status_code=404, detail='User not found or no valid data submitted')
    
    return {'status': status.HTTP_200_OK, 'message': 'User updated successfully!'}
