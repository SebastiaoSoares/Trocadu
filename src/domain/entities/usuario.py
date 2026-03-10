"""Módulo contendo a entidade Usuario para o jogo Trocadu."""

from uuid import UUID
from src.domain.shared.mixins import JsonSerializavelMixin

class Usuario(JsonSerializavelMixin):
    """Representa o cadastro persistente do utilizador com as suas preferências.

    Esta classe gere as informações de uma conta de utilizador que possui 
    registo no sistema, permitindo a persistência do seu histórico e a 
    criação de pacotes personalizados.

    Attributes:
        id (UUID): O identificador único (UUID) do utilizador no sistema.
        nickname (str): O nome de exibição escolhido pelo utilizador.
    """
    
    def __init__(self, id_usuario: UUID, nickname: str):
        """Inicializa um novo utilizador com os seus dados de cadastro.

        Args:
            id_usuario (UUID): O identificador único gerado para o utilizador.
            nickname (str): O nome de exibição inicial do utilizador.
        """
        self.id = id_usuario
        self.nickname = nickname

    def atualizar_perfil(self, novo_nickname: str) -> None:
        """Atualiza o nome de exibição do utilizador.

        Args:
            novo_nickname (str): O novo nickname que substituirá o atual.
        """
        self.nickname = novo_nickname
    
    def to_json(self) -> dict:
        """Converte os dados do utilizador para um dicionário serializável.

        Returns:
            dict: Um dicionário contendo o `id` (convertido para string) 
            e o `nickname` do utilizador.
        """
        return {
            "id": str(self.id),
            "nickname": self.nickname
        }