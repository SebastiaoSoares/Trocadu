"""
Define a entidade Palavra, a unidade básica de adivinhação do jogo.
"""

from src.domain.shared.mixins import JsonSerializavelMixin

class Palavra(JsonSerializavelMixin):
    """
    Entidade que representa a palavra a ser adivinhada no jogo.
    """

    def __init__(self, termo: str, dica: str = "", categoria: str = "Geral"):
        """
        Inicializa uma nova palavra com termo, dica e categoria.
        """
        self.__termo = termo
        self.__dica = dica
        self.categoria = categoria

    @property
    def termo(self) -> str:
        """
        Retorna o termo da palavra (somente leitura).
        """
        return self.__termo

    @property
    def dica(self) -> str:
        """
        Retorna a dica da palavra (somente leitura).
        """
        return self.__dica

    def __str__(self) -> str:
        """
        Retorna a representação em texto da palavra.
        """
        return f"{self.termo} ({self.categoria})"

    def to_dict(self):
        """
        Converte a palavra para dicionário, acessando os atributos privados.
        """
        return {
            "termo": self.termo,
            "dica": self.dica,
            "categoria": self.categoria
        }