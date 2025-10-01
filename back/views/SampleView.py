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
    data = data.model_copy(update={"id_user": user})
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


@router.put('/sample/{id}', status_code=status.HTTP_200_OK)
async def update_sample(id: str, data: dict, token: str = Depends(oauth2oscheme)):
    user = AuthController.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    if 'sample' in data:
        current = FullSampleSchema.get_sample(id)
        merged = current.model_dump()
        merged.update(data)

        results = SampleController.calculate_iqms_for_sample(FullSampleSchema(**merged))
        data = results.model_dump()

    updated = FullSampleSchema.update_sample(id, data)
    if not updated:
        raise HTTPException(status_code=404, detail='Sample not found')
    return {'message': 'Sample updated successfuly!'}


@router.delete('/sample/{id}', status_code=status.HTTP_200_OK)
async def delete_sample(id: str, token: str = Depends(oauth2oscheme)):
    user = AuthController.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    sample = FullSampleSchema.get_sample(id)
    if not sample:
        raise HTTPException(status_code=404, detail='Sample not found')
    deleted = FullSampleSchema.delete_sample(id)
    return {'message': 'Sample deleted successfuly!', 'deleted': deleted}


@router.get('/samples/user')
async def active_user_sample(token: str = Depends(oauth2oscheme)):
    user = AuthController.get_current_user(token)
    if not user:
        raise HTTPException(status_code=401, detail='Invalid credentials')
    data = FullSampleSchema.get_sample_active_user(str(user))
    return {'data': data}
