from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.models import PartidaModel
from src.infrastructure.security.auth import get_current_user_id
from src.infrastructure.api.v1.schemas.historico import PartidaHistoricoResponse

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[PartidaHistoricoResponse])
def listar_historico_usuario(
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """
    Retorna todas as partidas finalizadas pelo utilizador autenticado,
    ordenadas da mais recente para a mais antiga.
    """
    partidas = db.query(PartidaModel).filter(
        PartidaModel.usuario_id == usuario_id
    ).order_by(PartidaModel.data_jogada.desc()).all()
    
    return partidas
