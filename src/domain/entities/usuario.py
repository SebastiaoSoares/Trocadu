from uuid import UUID
from src.domain.shared.mixins import JsonSerializavelMixin

class Usuario(JsonSerializavelMixin):
    """
    Representa o cadastro persistente com preferências.
    """
    
    def __init__(self, id_usuario: UUID, nickname: str):
        self.id = id_usuario
        self.nickname = nickname

    def atualizar_perfil(self, novo_nickname: str):
        self.nickname = novo_nickname
    
    def to_json(self) -> dict:
        return {
            "id": str(self.id),
            "nickname": self.nickname
        }