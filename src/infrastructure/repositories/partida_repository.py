"""Módulo contendo a implementação do repositório de histórico de partidas."""

from sqlalchemy.orm import Session
from src.infrastructure.database.models import PartidaModel, ResultadoModel

class PartidaRepository:
    """Repositório para persistência do histórico e resultados das partidas.

    Isola a lógica de acesso a dados (SQLAlchemy) das regras de negócio do domínio,
    gerenciando as transações no banco de dados para salvar partidas e 
    suas respectivas pontuações finais.

    Attributes:
        session (Session): Sessão ativa do SQLAlchemy para comunicação com o banco.
    """
    
    def __init__(self, session: Session):
        """Inicializa o repositório com a sessão do banco de dados.

        Args:
            session (Session): Instância da sessão do SQLAlchemy (injetada).
        """
        self.session = session

    def salvar_historico(self, tipo_partida: str, ranking: list) -> None:
        """Salva uma nova partida e o ranking final dos jogadores no banco de dados.

        Cria um registro principal para a partida e, usando o ID gerado (via `flush`), 
        itera sobre o ranking para criar e vincular os resultados individuais de cada jogador. 
        Ao final, realiza o commit de toda a transação.

        Args:
            tipo_partida (str): O identificador do modo de jogo executado 
                (ex: 'COMPETITIVA_CLASSICA').
            ranking (list): Uma lista de dicionários com os resultados finais. 
                Cada dicionário deve conter as chaves 'nome' (str), 'pontos' (int) 
                e 'posicao' (int).
        """
        nova_partida = PartidaModel(tipo=tipo_partida)
        self.session.add(nova_partida)
        self.session.flush()

        for item in ranking:
            resultado = ResultadoModel(
                partida_id=nova_partida.id,
                nome_jogador=item['nome'],
                pontos=item['pontos'],
                posicao=item['posicao']
            )
            self.session.add(resultado)
        
        self.session.commit()