from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.models import PacoteModel, PalavraModel
from src.infrastructure.api.v1.schemas.pacote import PacoteCreate, PacoteUpdate, PacoteResponse
from src.infrastructure.security.auth import get_current_user_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=PacoteResponse, status_code=status.HTTP_201_CREATED)
def criar_pacote(
    pacote_in: PacoteCreate, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Cria um novo pacote de palavras vinculado ao utilizador autenticado."""
    novo_pacote = PacoteModel(
        usuario_id=usuario_id,
        nome=pacote_in.nome,
        descricao=pacote_in.descricao
    )
    db.add(novo_pacote)
    db.flush()

    palavras_db = [
        PalavraModel(
            pacote_id=novo_pacote.id,
            termo=p.termo,
            dica=p.dica,
            categoria=p.categoria
        )
        for p in pacote_in.palavras
    ]
    db.add_all(palavras_db)
    
    db.commit()
    db.refresh(novo_pacote)
    return novo_pacote

@router.get("/", response_model=List[PacoteResponse], status_code=status.HTTP_200_OK)
def listar_pacotes(
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Lista todos os pacotes pertencentes ao utilizador autenticado."""
    pacotes = db.query(PacoteModel).filter(PacoteModel.usuario_id == usuario_id).all()
    return pacotes

@router.get("/{pacote_id}", response_model=PacoteResponse, status_code=status.HTTP_200_OK)
def obter_pacote(
    pacote_id: int, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Retorna os detalhes de um pacote específico."""
    pacote = db.query(PacoteModel).filter(
        PacoteModel.id == pacote_id, 
        PacoteModel.usuario_id == usuario_id
    ).first()
    
    if not pacote:
        raise HTTPException(status_code=404, detail="Pacote não encontrado ou não pertence ao utilizador.")
    return pacote

@router.put("/{pacote_id}", response_model=PacoteResponse, status_code=status.HTTP_200_OK)
def atualizar_pacote(
    pacote_id: int, 
    pacote_in: PacoteUpdate, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Atualiza as informações de um pacote e substitui as suas palavras."""
    pacote = db.query(PacoteModel).filter(
        PacoteModel.id == pacote_id, 
        PacoteModel.usuario_id == usuario_id
    ).first()
    
    if not pacote:
        raise HTTPException(status_code=404, detail="Pacote não encontrado.")

    if pacote_in.nome is not None:
        pacote.nome = pacote_in.nome
    if pacote_in.descricao is not None:
        pacote.descricao = pacote_in.descricao

    if pacote_in.palavras is not None:
        db.query(PalavraModel).filter(PalavraModel.pacote_id == pacote_id).delete()
        
        novas_palavras = [
            PalavraModel(
                pacote_id=pacote_id,
                termo=p.termo,
                dica=p.dica,
                categoria=p.categoria
            ) for p in pacote_in.palavras
        ]
        db.add_all(novas_palavras)

    db.commit()
    db.refresh(pacote)
    return pacote

@router.delete("/{pacote_id}", status_code=status.HTTP_204_NO_CONTENT)
def deletar_pacote(
    pacote_id: int, 
    db: Session = Depends(get_db), 
    usuario_id: str = Depends(get_current_user_id)
):
    """Elimina um pacote e todas as suas palavras (via Cascade)."""
    pacote = db.query(PacoteModel).filter(
        PacoteModel.id == pacote_id, 
        PacoteModel.usuario_id == usuario_id
    ).first()
    
    if not pacote:
        raise HTTPException(status_code=404, detail="Pacote não encontrado.")

    db.delete(pacote)
    db.commit()
    return None
