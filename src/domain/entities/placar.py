from typing import List, Dict, Any

class Placar:
    """
    Responsável exclusivamente por processar e formatar rankings.
    """
    
    @staticmethod
    def processar_ranking(ranking_bruto: Dict[str, int]) -> List[Dict[str, Any]]:
        """
        Recebe {'Nome': pontos} e retorna lista ordenada para JSON.
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
        return ranking_processado[0] if ranking_processado else None