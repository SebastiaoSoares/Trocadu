from src.domain.shared.mixins import JsonSerializavelMixin
from src.domain.entities.jogador import Jogador

class Equipe(JsonSerializavelMixin):
    """
    Agrupa jogadores e gerencia a pontuação coletiva da partida.
    """
    
    def __init__(self, jogador_1: Jogador, jogador_2: Jogador):
        self.jogador_1 = jogador_1
        self.jogador_2 = jogador_2
        self.pontuacao_da_dupla = 0

    def registrar_pontos_rodada(self, pontos: int):
        self.pontuacao_da_dupla += pontos
        
        self.jogador_1.incrementar_pontos(pontos)
        self.jogador_2.incrementar_pontos(pontos)

    def to_json(self) -> dict:
        return {
            "jogador_1": self.jogador_1.nome,
            "jogador_2": self.jogador_2.nome,
            "pontuacao": self.pontuacao_da_dupla
        }
