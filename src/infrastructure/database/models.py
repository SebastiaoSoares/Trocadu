"""Módulo contendo os modelos de mapeamento relacional (ORM) do SQLAlchemy."""

import uuid
from datetime import datetime
from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.infrastructure.database.database import Base

class UsuarioModel(Base):
    """Modelo de representação da tabela de utilizadores no banco de dados.

    Armazena as credenciais de autenticação e os dados de perfil dos 
    jogadores que se registam no sistema do Trocadu.

    Attributes:
        id (str): Chave primária. Identificador único do utilizador gerado via UUID.
        email (str): Endereço de e-mail do utilizador (único e indexado).
        senha_hash (str): Hash criptográfico da palavra-passe do utilizador.
        nickname (str): Nome de exibição público escolhido pelo utilizador.
    """
    __tablename__ = "usuarios"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    senha_hash = Column(String, nullable=False)
    nickname = Column(String, nullable=False)

class JogadorSalvoModel(Base):
    """Modelo de representação da tabela de jogadores salvos.

    Permite que um utilizador autenticado guarde nomes de companheiros de
    jogo frequentes para facilitar a criação rápida de partidas futuras.

    Attributes:
        id (int): Chave primária. Identificador numérico do registo.
        usuario_id (str): Chave estrangeira referenciando o utilizador dono do registo.
        nome (str): O nome do jogador salvo.
    """
    __tablename__ = "jogadores_salvos"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)

class PacoteModel(Base):
    """Modelo de representação da tabela de pacotes de palavras.

    Permite agrupar um conjunto de palavras personalizadas criadas 
    por um utilizador específico para usar em partidas customizadas.

    Attributes:
        id (int): Chave primária numérica do pacote.
        usuario_id (str): Chave estrangeira referenciando o utilizador criador do pacote.
        nome (str): O título ou nome dado ao pacote.
        descricao (str): Uma breve descrição opcional sobre o tema do pacote.
        palavras (relationship): Relação um-para-muitos com `PalavraModel` (exclui em cascata).
    """
    __tablename__ = "pacotes"
    
    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    
    palavras = relationship("PalavraModel", back_populates="pacote", cascade="all, delete-orphan")

class PalavraModel(Base):
    """Modelo de representação da tabela de palavras personalizadas.

    Armazena os termos individuais que compõem um pacote criado por um utilizador.

    Attributes:
        id (int): Chave primária numérica da palavra.
        pacote_id (int): Chave estrangeira que vincula a palavra ao seu pacote.
        termo (str): O texto da palavra a ser adivinhada no jogo.
        pacote (relationship): Relação muitos-para-um de volta para `PacoteModel`.
    """
    __tablename__ = "palavras"
    
    id = Column(Integer, primary_key=True, index=True)
    pacote_id = Column(Integer, ForeignKey("pacotes.id"))
    termo = Column(String, nullable=False)
    
    pacote = relationship("PacoteModel", back_populates="palavras")

class PartidaModel(Base):
    """Modelo de representação da tabela de histórico de partidas.

    Guarda os metadados de uma partida finalizada por um utilizador, 
    incluindo o modo de jogo escolhido e o momento em que ocorreu.

    Attributes:
        id (str): Chave primária. Identificador único da partida gerado via UUID.
        usuario_id (str): Chave estrangeira que vincula a partida ao utilizador.
        modo_jogo (str): O identificador do modo jogado (ex: 'COMPETITIVA_CLASSICA').
        data_jogada (datetime): A data e hora exatas em que a partida foi registada.
        resultados (relationship): Relação um-para-muitos com `ResultadoModel` (exclui em cascata).
    """
    __tablename__ = "partidas"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    usuario_id = Column(String, ForeignKey("usuarios.id"), nullable=False)
    modo_jogo = Column(String, nullable=False)
    data_jogada = Column(DateTime, default=datetime.utcnow)

    resultados = relationship("ResultadoModel", back_populates="partida", cascade="all, delete-orphan")

class ResultadoModel(Base):
    """Modelo de representação da tabela de resultados de uma partida.

    Armazena a classificação final, equipas e pontuações associadas 
    a uma partida específica registada no histórico.

    Attributes:
        id (int): Chave primária numérica do resultado.
        partida_id (str): Chave estrangeira que vincula este resultado à sua partida.
        equipe (str): O nome da equipa ou jogador que pontuou.
        pontuacao (int): O total de pontos obtidos ao fim da partida.
        posicao (int): A posição final alcançada no ranking (ex: 1 para campeão).
        partida (relationship): Relação muitos-para-um de volta para `PartidaModel`.
    """
    __tablename__ = "resultados"
    
    id = Column(Integer, primary_key=True, index=True)
    partida_id = Column(String, ForeignKey("partidas.id"))
    equipe = Column(String, nullable=False)
    pontuacao = Column(Integer, nullable=False)
    posicao = Column(Integer, nullable=False)

    partida = relationship("PartidaModel", back_populates="resultados")