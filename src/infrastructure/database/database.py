from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.database.models import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./trocadu.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def criar_tabelas():
    Base.metadata.create_all(bind=engine)