"""Módulo contendo a entidade Jogador para o jogo Trocadu."""

from typing import Union
from src.domain.entities.usuario import Usuario

class Jogador:
    """Representa quem joga na partida atual.

    Esta classe gere o estado individual de um participante durante uma partida.
    Pode representar um jogador anónimo (local, definido apenas por um nome) 
    ou referenciar um `Usuario` autenticado no sistema.

    Attributes:
        nome (str): O nome de exibição do jogador na partida.
        usuario_ref (Usuario | None): A referência para a conta do utilizador, 
            caso o jogador esteja autenticado. Será `None` para jogadores locais.
        pontuacao_individual (int): A pontuação total acumulada pelo jogador 
            ao longo da partida.
    """
    
    def __init__(self, identificador: Union[Usuario, str]):
        """Inicializa um novo jogador.

        Configura o nome e a referência de utilizador baseando-se no tipo
        do identificador fornecido, e inicia a pontuação a zero.

        Args:
            identificador (Union[Usuario, str]): Pode ser um objeto `Usuario` 
                (para extrair o nickname e guardar a referência) ou uma `str` 
                (representando o nome de um jogador anónimo/local).
        """
        if isinstance(identificador, Usuario):
            self.nome = identificador.nickname
            self.usuario_ref = identificador
        else:
            self.nome = str(identificador)
            self.usuario_ref = None
            
        self.pontuacao_individual = 0

    def incrementar_pontos(self, qtd: int) -> None:
        """Adiciona uma quantidade específica de pontos ao jogador.

        Args:
            qtd (int): A quantidade de pontos a ser somada à pontuação individual.
        """
        self.pontuacao_individual += qtd

    def obter_nome(self) -> str:
        """Retorna o nome de exibição do jogador.

        Returns:
            str: O nome do jogador (seja o nickname do utilizador ou o nome local).
        """
        return self.nome