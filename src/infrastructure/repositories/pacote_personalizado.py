"""
Implementação de fonte de palavras personalizadas vinculadas a um usuário.
"""

from uuid import UUID
from typing import List
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras
from src.domain.entities.palavra import Palavra

class PacotePersonalizado(PacoteDePalavras):
    """
    Busca palavras criadas por um usuário específico autenticado.
    """

    def __init__(self, id_usuario: UUID):
        """
        Inicializa com o ID do usuário para futura busca no banco de dados.
        """
        self.id_usuario = id_usuario

    def obter_palavras(self) -> List[Palavra]:
        """
        Mock da busca de palavras do usuário. 
        """
        return [
            Palavra(termo="Programação", dica="O que você está fazendo", categoria="Tecnologia"),
            Palavra(termo="Python", dica="Linguagem usada no backend", categoria="Tecnologia")
        ]
