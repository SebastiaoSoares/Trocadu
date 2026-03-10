"""Módulo contendo o registo dinâmico dos modos de jogo."""

from typing import Dict, Type, Optional
from src.domain.interfaces.partida_base import GerenciadorDePartida

class PartidaRegistry:
    """Mantém o registo dos modos de jogo disponíveis no sistema.

    Utiliza o padrão de projeto Registry em conjunto com decorators para 
    permitir a adição dinâmica de novas subclasses de `GerenciadorDePartida` 
    sem a necessidade de alterar o código central da fábrica.

    Attributes:
        _modos_registrados (Dict[str, Type[GerenciadorDePartida]]): Dicionário 
            interno da classe que mapeia o identificador em texto do modo de jogo 
            à sua respetiva classe concreta.
    """
    
    _modos_registrados: Dict[str, Type[GerenciadorDePartida]] = {}

    @classmethod
    def registrar(cls, chave: str):
        """Decorator utilizado para registar uma classe de jogo no sistema.

        Exemplo de uso: `@PartidaRegistry.registrar("NOME_DO_MODO")` posicionado 
        logo acima da definição da classe do caso de uso.

        Args:
            chave (str): O nome único em string que identificará o modo de jogo.

        Returns:
            Callable: Uma função wrapper que recebe a classe concreta, 
            realiza o registo interno e devolve a própria classe para a execução.

        Raises:
            ValueError: Se a chave fornecida já se encontrar registada no sistema.
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
        """Busca a classe correspondente ao identificador fornecido.

        Args:
            chave (str): O identificador (nome) do modo de jogo procurado.

        Returns:
            Optional[Type[GerenciadorDePartida]]: A classe do gestor de partida 
            caso seja encontrada, ou `None` se a chave não existir no registo.
        """
        return cls._modos_registrados.get(chave.upper().strip())

    @classmethod
    def listar_modos(cls) -> list[str]:
        """Obtém uma lista com todos os modos de jogo atualmente registados.

        Returns:
            list[str]: Uma lista contendo as chaves (nomes) de todos os 
            modos disponíveis (bastante útil para gerar mensagens de erro 
            ou para endpoints de listagem na API).
        """
        return list(cls._modos_registrados.keys())