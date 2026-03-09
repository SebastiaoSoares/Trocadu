"""Módulo que define a entidade Palavra, a unidade básica de adivinhação do jogo."""

from src.domain.shared.mixins import JsonSerializavelMixin

class Palavra(JsonSerializavelMixin):
    """Entidade que representa a palavra a ser adivinhada no jogo.

    Attributes:
        categoria (str): O grupo temático ao qual a palavra pertence.
        termo (str): A palavra ou termo a ser adivinhado (acessível apenas como propriedade de leitura).
        dica (str): Dica opcional para auxiliar os jogadores (acessível apenas como propriedade de leitura).
    """

    def __init__(self, termo: str, dica: str = "", categoria: str = "Geral"):
        """Inicializa uma nova palavra com termo, dica e categoria.

        Args:
            termo (str): O texto da palavra a adivinhar.
            dica (str, optional): Texto de dica associada à palavra. O valor padrão é "".
            categoria (str, optional): A categoria temática da palavra. O valor padrão é "Geral".
        """
        self.__termo = termo
        self.__dica = dica
        self.categoria = categoria

    @property
    def termo(self) -> str:
        """Retorna o termo da palavra.

        Returns:
            str: O texto correspondente ao termo da palavra (somente leitura).
        """
        return self.__termo

    @property
    def dica(self) -> str:
        """Retorna a dica da palavra.

        Returns:
            str: O texto correspondente à dica da palavra (somente leitura).
        """
        return self.__dica

    def __str__(self) -> str:
        """Retorna a representação em texto da palavra.

        Returns:
            str: Uma string formatada contendo o termo e a categoria da palavra.
        """
        return f"{self.termo} ({self.categoria})"

    def to_dict(self) -> dict:
        """Converte a palavra para dicionário, acedendo aos atributos privados através das propriedades.

        Returns:
            dict: Um dicionário contendo as chaves 'termo', 'dica' e 'categoria' 
            com os respetivos valores da palavra.
        """
        return {
            "termo": self.termo,
            "dica": self.dica,
            "categoria": self.categoria
        }