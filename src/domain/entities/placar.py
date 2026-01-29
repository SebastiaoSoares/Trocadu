from typing import List, Dict
from src.dominio.equipe import Equipe
from src.dominio.jogador import Jogador # <--- Adicione esse import

class Placar:
    """
    Responsável por exibir o ranking.
    """
    
    def exibir_ranking_duplas(self, equipes: List[Equipe]) -> Dict[str, int]:
        print("\n=== MELHORES DUPLAS ===")
        ranking = {}
        equipes_ordenadas = sorted(equipes, key=lambda e: e.pontuacao_da_dupla, reverse=True)
        
        for i, eq in enumerate(equipes_ordenadas, 1):
            nome_dupla = f"{eq.jogador_1.obter_nome()} & {eq.jogador_2.obter_nome()}"
            pontos = eq.pontuacao_da_dupla
            ranking[nome_dupla] = pontos
            print(f"{i}º Lugar: {nome_dupla} - {pontos} pts")
        return ranking

    def exibir_ranking_individual(self, jogadores: List[Jogador]) -> Dict[str, int]:
        print("\n=== CLASSIFICAÇÃO GERAL (INDIVIDUAL) ===")
        ranking = {}
        jogadores_ordenados = sorted(jogadores, key=lambda j: j.pontuacao_individual, reverse=True)
        
        for i, jog in enumerate(jogadores_ordenados, 1):
            nome = jog.obter_nome()
            pontos = jog.pontuacao_individual
            ranking[nome] = pontos
            print(f"{i}º Lugar: {nome} - {pontos} pts")
        return ranking