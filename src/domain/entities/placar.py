"""Módulo contendo a entidade Placar para o processamento de pontuações."""

from typing import List, Dict, Any

class Placar:
    """Responsável exclusivamente por processar e formatar rankings.

    Esta classe atua como um serviço utilitário para converter dados brutos de 
    pontuação em estruturas ordenadas e prontas para serem serializadas em JSON
    e devolvidas pela API.
    """
    
    @staticmethod
    def processar_ranking(ranking_bruto: Dict[str, int]) -> List[Dict[str, Any]]:
        """Ordena o ranking e adiciona a posição de cada jogador.

        Recebe um dicionário mapeando o nome do jogador à sua pontuação total, 
        ordena-o de forma decrescente (do maior para o menor) e converte-o numa 
        lista estruturada.

        Args:
            ranking_bruto (Dict[str, int]): Dicionário com o formato `{'Nome': pontos}`.

        Returns:
            List[Dict[str, Any]]: Uma lista de dicionários onde cada elemento contém 
            as chaves 'posicao' (int), 'nome' (str) e 'pontos' (int), ordenada pelos pontos.
        """
        ranking_ordenado = sorted(
            ranking_bruto.items(), 
            key=lambda item: item[1], 
            reverse=True
        )
        
        return [
            {"posicao": i, "nome": nome, "pontos": pontos}
            for i, (nome, pontos) in enumerate(ranking_ordenado, start=1)
        ]

    @staticmethod
    def obter_campeao(ranking_processado: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Extrai os dados do primeiro classificado no ranking.

        Args:
            ranking_processado (List[Dict[str, Any]]): A lista ordenada retornada 
                pelo método `processar_ranking`.

        Returns:
            Dict[str, Any]: O dicionário contendo os dados do campeão (1º lugar). 
            Retorna `None` se a lista de ranking estiver vazia.
        """
        return ranking_processado[0] if ranking_processado else None