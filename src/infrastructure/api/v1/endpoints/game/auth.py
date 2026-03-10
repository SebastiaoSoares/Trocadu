from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.models import UsuarioModel
from src.infrastructure.security.auth import verificar_senha, obter_hash_senha, criar_token_acesso, get_current_user_id

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UsuarioCreate(BaseModel):
    email: EmailStr
    senha: str
    nickname: str

class UsuarioResponse(BaseModel):
    id: str
    email: EmailStr
    nickname: str

    class Config:
        from_attributes = True

@router.get("/me", response_model=UsuarioResponse, status_code=status.HTTP_200_OK)
def obter_usuario_logado(
    usuario_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    Retorna os dados do utilizador atualmente logado. 
    Se o token for inválido, o FastAPI barra a requisição automaticamente com erro 401.
    """
    usuario = db.query(UsuarioModel).filter(UsuarioModel.id == usuario_id).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Utilizador não encontrado no sistema.")
        
    return usuario

@router.post("/registrar", status_code=status.HTTP_201_CREATED)
def registrar_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    usuario_existente = db.query(UsuarioModel).filter(UsuarioModel.email == usuario.email).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="E-mail já registado.")
        
    novo_usuario = UsuarioModel(
        email=usuario.email,
        senha_hash=obter_hash_senha(usuario.senha),
        nickname=usuario.nickname
    )
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)
    return {"mensagem": "Usuário criado com sucesso!", "id": novo_usuario.id}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    usuario = db.query(UsuarioModel).filter(UsuarioModel.email == form_data.username).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
    
    if not verificar_senha(form_data.password, usuario.senha_hash):
        raise HTTPException(status_code=401, detail="E-mail ou senha incorretos")
        
    token_acesso = criar_token_acesso(dados={"sub": usuario.id})
    return {"access_token": token_acesso, "token_type": "bearer"}
