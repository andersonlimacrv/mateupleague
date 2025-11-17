from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/leitura-ambiente", tags=["API Test - Leituras"])

class TestSchema(BaseModel):
    Message: str


@router.post("")
async def post_test(payload: TestSchema):
    print(payload.model_dump())
    return {"message": "Leitura de ambiente recebida com sucesso"}
