from typing import List
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.entities.jogador import Jogador

class PartidaFactory:
    @staticmethod
    def criar_partida(tipo: str, pool_jogadores: List[Jogador], banco_palavras: object) -> GerenciadorDePartida:
        
        classe_concreta = PartidaRegistry.obter_classe(tipo)

        if not classe_concreta:
             modos = PartidaRegistry.listar_modos()
             raise ValueError(f"Modo '{tipo}' inválido. Disponíveis: {modos}")

        return classe_concreta(pool_jogadores, banco_palavras)