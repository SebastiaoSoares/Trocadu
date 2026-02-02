"""
Interface para as estratégias de obtenção de palavras.
"""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.palavra import Palavra

class PacoteDePalavras(ABC):
    """
    Define o contrato obrigatório para qualquer fonte de palavras.
    """

    @abstractmethod
    def obter_palavras(self) -> List[Palavra]:
        """
        Retorna uma lista de objetos Palavra.
        """
        pass