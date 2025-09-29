from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from models.SampleModel import FullSampleSchema
from controller.SampleController import SampleController
from controller.AuthController import AuthController

router = APIRouter()
oauth2oscheme = OAuth2PasswordBearer(tokenUrl='token')

@router.post('/sample', status_code=status.HTTP_201_CREATED)
async def create_sample(data: FullSampleSchema, token: str = Depends(oauth2oscheme)):
    user = AuthController.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    results = SampleController.calculate_iqms_for_sample(data)
    inserted_id = FullSampleSchema.create_sample(results)
    return {'message': 'Sample created successfully!', 'sample_id': inserted_id}


@router.get('/sample/{id}', status_code=status.HTTP_200_OK)
async def get_sample(id: str, token: str = Depends(oauth2oscheme)):
    user = AuthController.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    sample = FullSampleSchema.get_sample(id)
    return {'sample': sample}
