from fastapi import APIRouter, status

from src.domain.registry.partida_registry import PartidaRegistry

router = APIRouter()

@router.get("/modos", status_code=status.HTTP_200_OK)
def game_modes():
    """Lista os modos de jogo registrados na aplicação."""
    return {"modos_disponiveis": PartidaRegistry.listar_modos()}
