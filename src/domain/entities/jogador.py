from typing import Union
from src.domain.entities.usuario import Usuario

class Jogador:
    """
    Representa quem joga na partida atual.
    Pode ser um jogador anônimo (local) ou referenciar um Usuario autenticado.
    """
    
    def __init__(self, identificador: Union[Usuario, str]):
        if isinstance(identificador, Usuario):
            self.nome = identificador.nickname
            self.usuario_ref = identificador
        else:
            self.nome = str(identificador)
            self.usuario_ref = None
            
        self.pontuacao_individual = 0

    def incrementar_pontos(self, qtd: int):
        self.pontuacao_individual += qtd

    def obter_nome(self) -> str:
        return self.nome