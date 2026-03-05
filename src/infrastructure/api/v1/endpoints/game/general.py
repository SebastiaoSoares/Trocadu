from fastapi import APIRouter

from src.domain.registry.partida_registry import PartidaRegistry

router = APIRouter()

@router.get("/status")
def game_status():
    """Retorna o status operacional do módulo de jogo."""
    return {"status": "operacional"}

@router.get("/modes")
def game_modes():
    """Lista os modos de jogo registrados na aplicação."""
    return {"modos_disponiveis": PartidaRegistry.listar_modos()}
