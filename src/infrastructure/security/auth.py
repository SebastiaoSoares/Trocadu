import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta_fallback")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # Token válido por 7 dias

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/game/auth/login")
oauth2_scheme_opcional = OAuth2PasswordBearer(tokenUrl="/game/auth/login", auto_error=False)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara a senha em texto com o hash guardado no banco."""
    senha_bytes = senha_plana.encode('utf-8')
    hash_bytes = senha_hash.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)

def obter_hash_senha(senha: str) -> str:
    """Gera o hash da senha usando bcrypt puro."""
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return senha_hash_bytes.decode('utf-8')

def criar_token_acesso(dados: dict) -> str:
    dados_a_codificar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_a_codificar.update({"exp": expiracao})
    
    token_jwt = jwt.encode(dados_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    excecao_credenciais = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id_usuario: str = payload.get("sub")
        if id_usuario is None:
            raise excecao_credenciais
        return id_usuario
    except jwt.PyJWTError:
        raise excecao_credenciais

def get_current_user_id_optional(token: Optional[str] = Depends(oauth2_scheme_opcional)) -> Optional[str]:
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None