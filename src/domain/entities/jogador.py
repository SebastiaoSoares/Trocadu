from src.domain.entities.usuario import Usuario

class Jogador:
    """
    Representa quem joga na partida atual.
    """
    
    def __init__(self, nome: str):
        self.nome = nome
        self.pontuacao_individual = 0

    def incrementar_pontos(self, qtd: int):
        self.pontuacao_individual += qtd

    def obter_nome(self) -> str:
        return self.usuario_ref.nickname