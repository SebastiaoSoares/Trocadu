"""Módulo contendo a entidade Equipe para o jogo Trocadu."""

from src.domain.shared.mixins import JsonSerializavelMixin
from src.domain.entities.jogador import Jogador

class Equipe(JsonSerializavelMixin):
   """Agrupa jogadores e gere a pontuação coletiva da partida.

    Esta entidade é responsável por manter a associação entre os jogadores
    de uma dupla temporária e contabilizar os pontos obtidos em conjunto
    durante a rodada.

    Attributes:
        jogador_1 (Jogador): A instância do primeiro jogador da equipe.
        jogador_2 (Jogador): A instância do segundo jogador da equipe.
        pontuacao_da_dupla (int): Os pontos totais acumulados pela equipe.
    """
    
    def __init__(self, jogador_1: Jogador, jogador_2: Jogador):
        """Inicializa uma nova equipe com dois jogadores e pontuação a zero.

        Args:
            jogador_1 (Jogador): O primeiro jogador a compor a equipe.
            jogador_2 (Jogador): O segundo jogador a compor a equipe.
        """

        self.jogador_1 = jogador_1
        self.jogador_2 = jogador_2
        self.pontuacao_da_dupla = 0

    def registrar_pontos_rodada(self, pontos: int) -> None:
        """Regista a pontuação obtida na rodada para a equipe e para os jogadores.

        Adiciona a pontuação ao total da equipe e invoca a atualização 
        individual dos pontos para ambos os membros da dupla.

        Args:
            pontos (int): A quantidade de pontos a ser adicionada.
        """
        self.pontuacao_da_dupla += pontos
        
        self.jogador_1.incrementar_pontos(pontos)
        self.jogador_2.incrementar_pontos(pontos)
  

    def to_json(self) -> dict:
        """Converte os dados da equipe para um formato dicionário serializável.

        Returns:
            dict: Um dicionário com os nomes dos jogadores e a pontuação atual.
        """
        return {
            "jogador_1": self.jogador_1.nome,
            "jogador_2": self.jogador_2.nome,
            "pontuacao": self.pontuacao_da_dupla
        }