from typing import List
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.use_cases.partida_competitiva_classica import PartidaCompetitivaClassica
from src.domain.use_cases.partida_treino_classica import PartidaTreinoClassica
from src.domain.entities.jogador import Jogador
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras

class PartidaFactory:
    """
    Responsável por instanciar a estratégia de jogo correta baseada no tipo solicitado.
    """

    @staticmethod
    def criar_partida(tipo: str, pool_jogadores: List[Jogador], banco_palavras: PacoteDePalavras) -> GerenciadorDePartida:
        """
        Retorna uma instância concreta de GerenciadorDePartida.
        """
        modos_disponiveis = {
            "COMPETITIVA_CLASSICA": PartidaCompetitivaClassica,
            "TREINO_CLASSICA": PartidaTreinoClassica
        }

        tipo_upper = tipo.upper().strip()

        if tipo_upper not in modos_disponiveis:
            raise ValueError(f"Tipo de partida inválido: {tipo}. Modos: {list(modos_disponiveis.keys())}")

        classe_selecionada = modos_disponiveis[tipo_upper]

        return classe_selecionada(pool_jogadores, banco_palavras)
