import os
from fastapi import APIRouter

from src.infrastructure.api.v1.endpoints.game_routes import router as game
from src.infrastructure.api.v1.endpoints.partida_routes import router as partida

router = APIRouter()

@router.get("/", tags=["Geral"])
def health_check():
    """Verifica a integridade e o ambiente da API."""
    return {"status": f"Trocadu API online! Ambiente: {os.getenv('ENV', 'desenvolvimento')}"}

router.include_router(game, prefix="/game")
router.include_router(partida, prefix="/partida")