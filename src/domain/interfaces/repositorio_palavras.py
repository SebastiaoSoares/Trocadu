"""Módulo contendo a interface para as estratégias de obtenção de palavras."""

from abc import ABC, abstractmethod
from typing import List
from src.domain.entities.palavra import Palavra

class PacoteDePalavras(ABC):
    """Define o contrato obrigatório para qualquer fonte de palavras.

    Esta classe abstrata funciona como uma interface (Padrão Strategy) que 
    garante que qualquer repositório de palavras (seja um arquivo estático, 
    banco de dados ou API externa) implemente a estrutura necessária para 
    fornecer dados ao jogo.
    """

    @abstractmethod
    def obter_palavras(self) -> List[Palavra]:
        """Obtém o conjunto de palavras disponíveis na fonte de dados.

        Returns:
            List[Palavra]: Uma lista contendo as instâncias da entidade `Palavra` 
            carregadas a partir da fonte concreta implementada.
        """
        pass