"""Módulo contendo a fábrica para criação de instâncias de partidas."""

from typing import List, Optional
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.entities.jogador import Jogador
from src.domain.entities.configuracao import ConfiguracaoDePartida

import src.domain.use_cases

class PartidaFactory:
    """Fábrica responsável por instanciar os diferentes modos de jogo.

    Aplica o padrão de projeto Factory Method para encapsular a lógica de 
    criação das partidas. O cliente (ex: uma rota da API) não precisa 
    instanciar as classes concretas diretamente, bastando solicitar o 
    modo de jogo desejado através de uma string (chave).
    """

    @staticmethod
    def criar_partida(
        tipo: str, 
        pool_jogadores: List[Jogador], 
        banco_palavras: object,
        configuracao: Optional[ConfiguracaoDePartida] = None
    ) -> GerenciadorDePartida:
        """Cria e retorna uma instância do gestor de partida apropriado.

        Consulta o `PartidaRegistry` para encontrar a classe correspondente
        ao `tipo` solicitado e inicializa-a com os parâmetros fornecidos.

        Args:
            tipo (str): O identificador do modo de jogo (ex: "COMPETITIVA_CLASSICA").
            pool_jogadores (List[Jogador]): Lista de jogadores que participarão.
            banco_palavras (object): A fonte de palavras instanciada para o jogo.
            configuracao (ConfiguracaoDePartida, optional): Configurações de 
                tempo e limites da partida.

        Returns:
            GerenciadorDePartida: Uma instância da classe concreta que gere 
            o modo de jogo solicitado.

        Raises:
            ValueError: Se o `tipo` fornecido não estiver registado no sistema,
            retornando na mensagem de erro quais são os modos disponíveis.
        """
        
        classe_concreta = PartidaRegistry.obter_classe(tipo)

        if not classe_concreta:
             modos = PartidaRegistry.listar_modos()
             raise ValueError(f"Modo '{tipo}' inválido. Disponíveis: {modos}")

        return classe_concreta(pool_jogadores, banco_palavras, configuracao)