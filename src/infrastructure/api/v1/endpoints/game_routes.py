from fastapi import APIRouter

from src.infrastructure.api.v1.endpoints.game.general import router as general
from src.infrastructure.api.v1.endpoints.game.auth import router as auth
from src.infrastructure.api.v1.endpoints.pacotes import router as pacotes
from src.infrastructure.api.v1.endpoints.jogadores_salvos import router as jogadores
from src.infrastructure.api.v1.endpoints.historico_routes import router as historico

router = APIRouter()

router.include_router(general, tags=["Game"])

router.include_router(auth, prefix="/auth", tags=["Autenticação"])
router.include_router(pacotes, prefix="/pacotes", tags=["Pacotes Personalizados"])
router.include_router(jogadores, prefix="/jogadores", tags=["Jogadores Salvos"])
router.include_router(historico, prefix="/historico", tags=["Histórico de Partidas"])