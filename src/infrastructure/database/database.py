"""Módulo de configuração da conexão com a base de dados."""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./trocadu.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def criar_tabelas() -> None:
    """Gera as tabelas na base de dados a partir dos modelos definidos.

    Este método é invocado para garantir que toda a estrutura de tabelas
    necessária do SQLAlchemy seja criada no banco SQLite antes de qualquer 
    operação de leitura ou escrita ser realizada.
    """
    Base.metadata.create_all(bind=engine)