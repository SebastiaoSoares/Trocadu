import os
from fastapi import APIRouter
from src.domain.shared.factories import PartidaFactory

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": f"Trocadu API online! Ambiente: {os.getenv('ENV')}"}
