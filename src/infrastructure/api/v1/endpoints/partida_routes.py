from fastapi import APIRouter

from src.infrastructure.api.v1.endpoints.partida.classica_competitiva import router as classica_competitiva
from src.infrastructure.api.v1.endpoints.partida.classica_treino import router as classica_treino

router = APIRouter()

router.include_router(classica_competitiva, prefix="/classica-competitiva", tags=["Clássica Competitiva"])
router.include_router(classica_treino, prefix="/classica-treino", tags=["Clássica Treino"])
