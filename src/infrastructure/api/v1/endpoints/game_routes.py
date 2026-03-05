from fastapi import APIRouter

from src.infrastructure.api.v1.endpoints.game.general import router as general

router = APIRouter()

router.include_router(general, prefix="/game", tags=["Game"])
