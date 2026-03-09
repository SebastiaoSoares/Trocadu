"""Módulo responsável pela segurança, criptografia de senhas e gestão de tokens JWT."""

import os
import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

# Configurações de segurança e expiração
SECRET_KEY = os.getenv("SECRET_KEY", "chave_super_secreta_fallback")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # Token válido por 7 dias

# Esquemas de dependência do FastAPI para extrair o token do cabeçalho
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/game/auth/login")
oauth2_scheme_opcional = OAuth2PasswordBearer(tokenUrl="/game/auth/login", auto_error=False)

def verificar_senha(senha_plana: str, senha_hash: str) -> bool:
    """Compara a senha em texto plano com o hash guardado no banco de dados.

    Utiliza a biblioteca bcrypt para verificar a correspondência de forma segura,
    protegendo contra ataques de temporização (timing attacks).

    Args:
        senha_plana (str): A senha original digitada pelo utilizador.
        senha_hash (str): O hash bcrypt previamente armazenado na base de dados.

    Returns:
        bool: True se a senha fornecida corresponder ao hash, False caso contrário.
    """
    senha_bytes = senha_plana.encode('utf-8')
    hash_bytes = senha_hash.encode('utf-8')
    return bcrypt.checkpw(senha_bytes, hash_bytes)

def obter_hash_senha(senha: str) -> str:
    """Gera o hash criptográfico de uma senha usando bcrypt puro.

    Cria um salt aleatório e aplica o algoritmo de hashing para garantir 
    que as senhas dos utilizadores do Trocadu não sejam salvas em texto plano.

    Args:
        senha (str): A senha em texto plano a ser encriptada.

    Returns:
        str: O hash gerado em formato de string (decodificado de bytes), 
        pronto para ser guardado na base de dados.
    """
    senha_bytes = senha.encode('utf-8')
    salt = bcrypt.gensalt()
    senha_hash_bytes = bcrypt.hashpw(senha_bytes, salt)
    return senha_hash_bytes.decode('utf-8')

def criar_token_acesso(dados: dict) -> str:
    """Cria um token JWT de acesso com tempo de expiração configurado.

    Args:
        dados (dict): O payload contendo as informações a serem codificadas no 
            token (geralmente contendo o ID do utilizador na chave 'sub').

    Returns:
        str: O token JWT gerado e assinado digitalmente com a `SECRET_KEY`.
    """
    dados_a_codificar = dados.copy()
    expiracao = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    dados_a_codificar.update({"exp": expiracao})
    
    token_jwt = jwt.encode(dados_a_codificar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    """Obtém e valida o ID do utilizador autenticado a partir do token JWT.

    Esta função atua como uma dependência restrita para as rotas do FastAPI, 
    garantindo que apenas utilizadores com tokens válidos possam acessá-las.

    Args:
        token (str): O token JWT extraído automaticamente do cabeçalho de 
            autorização da requisição.

    Returns:
        str: O identificador único do utilizador (ID) decodificado do token.

    Raises:
        HTTPException: Erro 401 (Unauthorized) se o token for inválido, 
            estiver expirado ou não contiver o ID (campo 'sub').
    """
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
    """Tenta obter o ID do utilizador a partir do token de forma opcional.

    Útil para endpoints mistos que possuem comportamentos extras caso o 
    utilizador esteja logado (por exemplo, permitir o uso de pacotes de 
    palavras personalizados se autenticado, ou usar o pacote padrão se anónimo).

    Args:
        token (Optional[str]): O token JWT do cabeçalho, caso tenha sido enviado.

    Returns:
        Optional[str]: O ID do utilizador decodificado do token, ou `None` 
        se nenhum token for enviado ou se o token presente for inválido.
    """
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.PyJWTError:
        return None