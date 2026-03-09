import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class UsuarioModel(Base):
    __tablename__ = "usuarios"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nickname = Column(String, nullable=False)

class JogadorSalvoModel(Base):
    __tablename__ = "jogadores_salvos"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)

class PacoteModel(Base):
    __tablename__ = "pacotes"
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    
    palavras = relationship("PalavraModel", back_populates="pacote", cascade="all, delete-orphan")

class PalavraModel(Base):
    __tablename__ = "palavras"
    id = Column(Integer, primary_key=True, index=True)
    pacote_id = Column(Integer, ForeignKey("pacotes.id"))
    termo = Column(String, nullable=False)
    
    pacote = relationship("PacoteModel", back_populates="palavras")

class PartidaModel(Base):
    __tablename__ = "partidas"
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    modo_jogo = Column(String, nullable=False)
    data_jogada = Column(DateTime, default=datetime.utcnow)

    resultados = relationship("ResultadoModel", back_populates="partida", cascade="all, delete-orphan")

class ResultadoModel(Base):
    __tablename__ = "resultados"
    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(String, ForeignKey("partidas.id"))
    equipe = Column(String, nullable=False)
    pontuacao = Column(Integer, nullable=False)
    posicao = Column(Integer, nullable=False)

    partida = relationship("PartidaModel", back_populates="resultados")
