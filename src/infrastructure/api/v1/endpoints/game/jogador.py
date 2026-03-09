from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.models import JogadorSalvoModel
from src.infrastructure.security.auth import get_current_user_id
from src.infrastructure.api.v1.schemas.jogador_salvo import (
    JogadorSalvoCreate, 
    JogadorSalvoUpdate, 
    JogadorSalvoResponse
)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=JogadorSalvoResponse, status_code=status.HTTP_201_CREATED)
def adicionar_jogador(
    jogador_in: JogadorSalvoCreate, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Adiciona um novo jogador à lista de amigos do utilizador autenticado."""
    jogador_existente = db.query(JogadorSalvoModel).filter(
        JogadorSalvoModel.usuario_id == usuario_id,
        JogadorSalvoModel.nome == jogador_in.nome
    ).first()
    
    if jogador_existente:
        raise HTTPException(status_code=400, detail="Este jogador já está na tua lista.")

    novo_jogador = JogadorSalvoModel(
        usuario_id=usuario_id,
        nome=jogador_in.nome
    )
    db.add(novo_jogador)
    db.commit()
    db.refresh(novo_jogador)
    return novo_jogador

@router.get("/", response_model=List[JogadorSalvoResponse], status_code=status.HTTP_200_OK)
def listar_jogadores(
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Lista todos os jogadores salvos pelo utilizador autenticado."""
    jogadores = db.query(JogadorSalvoModel).filter(JogadorSalvoModel.usuario_id == usuario_id).all()
    return jogadores

@router.get("/{jogador_id}", response_model=JogadorSalvoResponse, status_code=status.HTTP_200_OK)
def obter_jogador(
    jogador_id: int, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Retorna os detalhes de um jogador salvo específico."""
    jogador = db.query(JogadorSalvoModel).filter(
        JogadorSalvoModel.id == jogador_id, 
        JogadorSalvoModel.usuario_id == usuario_id
    ).first()
    
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")
    return jogador

@router.put("/{jogador_id}", response_model=JogadorSalvoResponse, status_code=status.HTTP_200_OK)
def atualizar_jogador(
    jogador_id: int, 
    jogador_in: JogadorSalvoUpdate, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Atualiza o nome de um jogador salvo."""
    jogador = db.query(JogadorSalvoModel).filter(
        JogadorSalvoModel.id == jogador_id, 
        JogadorSalvoModel.usuario_id == usuario_id
    ).first()
    
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")

    jogador.nome = jogador_in.nome
    db.commit()
    db.refresh(jogador)
    return jogador

@router.delete("/{jogador_id}", status_code=status.HTTP_204_NO_CONTENT)
def remover_jogador(
    jogador_id: int, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Remove um jogador da lista do utilizador."""
    jogador = db.query(JogadorSalvoModel).filter(
        JogadorSalvoModel.id == jogador_id, 
        JogadorSalvoModel.usuario_id == usuario_id
    ).first()
    
    if not jogador:
        raise HTTPException(status_code=404, detail="Jogador não encontrado.")

    db.delete(jogador)
    db.commit()
    return None
    