from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class UsuarioModel(Base):
    __tablename__ = 'usuarios'
    id = Column(String, primary_key=True)
    nickname = Column(String, nullable=False)

class PartidaModel(Base):
    __tablename__ = 'partidas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo = Column(String, nullable=False)
    data_hora = Column(DateTime, default=datetime.utcnow)
    resultados = relationship("ResultadoModel", back_populates="partida")

class ResultadoModel(Base):
    __tablename__ = 'resultados'
    id = Column(Integer, primary_key=True, autoincrement=True)
    partida_id = Column(Integer, ForeignKey('partidas.id'))
    nome_jogador = Column(String, nullable=False)
    pontos = Column(Integer, default=0)
    posicao = Column(Integer)
    partida = relationship("PartidaModel", back_populates="resultados")