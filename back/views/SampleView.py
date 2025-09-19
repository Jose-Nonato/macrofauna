from fastapi import APIRouter, HTTPException, status
from models.SampleModel import SampleSchema
from models.UserModel import UserModel


router = APIRouter()


@router.post('/sample', status_code=status.HTTP_201_CREATED)
def create_sample(data: SampleSchema):
    sample_dict = data.model_dump()
    # Adicionar validação de imagem em base64!
    sample_id = SampleSchema.create_sample(sample_dict)
    return {'message': 'Sample created successfully!', 'id': sample_id}
