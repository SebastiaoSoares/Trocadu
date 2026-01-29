"""
Mixins utilitários para serialização e funcionalidades compartilhadas.
"""

import json
from typing import Any, Dict

class JsonSerializavelMixin:
    """
    Mixin para converter objetos em JSON e vice-versa.
    """

    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o objeto para dicionário.
        """
        return self.__dict__

    def to_json(self) -> str:
        """
        Serializa para string JSON.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, json_str: str):
        """
        Reconstrói o objeto a partir do JSON.
        """
        dados = json.loads(json_str)
        return cls(**dados)