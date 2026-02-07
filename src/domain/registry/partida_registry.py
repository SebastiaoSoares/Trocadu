from typing import Dict, Type, Optional
from src.domain.interfaces.partida_base import GerenciadorDePartida

class PartidaRegistry:
    """
    Mentém registro dos modos de jogo disponíveis.
    Utiliza o padrão Registry com decorators.
    """
    
    _modos_registrados: Dict[str, Type[GerenciadorDePartida]] = {}

    @classmethod
    def registrar(cls, chave: str):
        """
        Decorator para registrar uma classe de jogo.
        Uso: @PartidaRegistry.registrar("NOME_DO_MODO")
        """
        def wrapper(classe_concreta: Type[GerenciadorDePartida]):
            chave_upper = chave.upper().strip()
            
            if chave_upper in cls._modos_registrados:
                raise ValueError(f"O modo '{chave_upper}' já está registrado.")
            
            cls._modos_registrados[chave_upper] = classe_concreta
            return classe_concreta
        return wrapper

    @classmethod
    def obter_classe(cls, chave: str) -> Optional[Type[GerenciadorDePartida]]:
        """
        Retorna a classe correspondente à chave, ou None se não existir.
        """
        return cls._modos_registrados.get(chave.upper().strip())

    @classmethod
    def listar_modos(cls) -> list[str]:
        """
        Retorna a lista de chaves registradas (útil para mensagens de erro).
        """
        return list(cls._modos_registrados.keys())
