from src.domain.entities.placar import Placar
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.shared.mixins import PermutadorMixin
from typing import Any, Dict

@PartidaRegistry.registrar("COMPETITIVA_CLASSICA")
class PartidaCompetitivaClassica(PermutadorMixin, GerenciadorDePartida):
    """
    Implementação oficial do jogo valendo pontos e ranking.
    - Múltiplos Jogadores (3 ou mais).
    - Todos jogam contra todos uma vez (ida e volta).
    - Ganha quem fizer mais pontos no total.
    - Ranking final exibido ao término.
    """

    def __init__(self, pool_jogadores: list, pacote_palavras: object):
        super().__init__(pool_jogadores, pacote_palavras)
        self._ranking: Dict[str, int] = {}
        self._dupla_atual = None

    def _setup(self):
        self._fila_de_duplas = self._gerar_permutacoes_duplas()
        self._ranking = {jogador.nome: 0 for jogador in self._pool_jogadores}

    def computar_pontos_rodada(self, pontos_conquistados: int):
        """
        Atribui a pontuação da rodada para ambos os jogadores da dupla atual.
        """
        
        if not self._turno_atual or not self._turno_atual.dupla:
            raise ValueError("Não há rodada ativa para pontuar.")

        nome_j1 = self._turno_atual.dupla.jogador_1.nome
        nome_j2 = self._turno_atual.dupla.jogador_2.nome

        if nome_j1 in self._ranking:
            self._ranking[nome_j1] += pontos_conquistados
        
        if nome_j2 in self._ranking:
            self._ranking[nome_j2] += pontos_conquistados

        return {
            "mensagem": f"Pontos computados: +{pontos_conquistados} para {nome_j1} e {nome_j2}",
            "ranking_atual": self._ranking
        }

    def avancar(self) -> Dict[str, Any]:

        if self._status != self.Status.EM_ANDAMENTO:
             return {"erro": "A partida precisa ser iniciada antes de avançar."}

        # se a fila estiver vazia, encerra o jogo
        if not self._fila_de_duplas:
            self._status = self.Status.FINALIZADO
            resultado_final = self._processar_vitoria()
            return {
                "status": "FINALIZADO",
                "dados": resultado_final
            }

        # se tiver gente na fila, avança e retira o próximo par
        dupla_atual = self._fila_de_duplas.popleft()
        
        # troca o turno
        self._executar_rodada_ida_e_volta(dupla_atual)

        return {
            "status": "RODADA_NOVA",
            "dupla": {
                "jogador1": dupla_atual.jogador_1.nome,
                "jogador2": dupla_atual.jogador_2.nome
            },
            "palavra": self._turno_atual.palavra_atual,
            "tempo_limite": self._turno_atual.tempo_limite
        }

    def _processar_vitoria(self):
        """
        Finaliza a partida, ordena o ranking e retorna o sumário.
        """

        self._status = self.Status.FINALIZADO

        ranking_formatado = Placar.processar_ranking(self._ranking)
        campeao = Placar.obter_campeao(ranking_formatado)

        return {
            "mensagem": "Torneio encerrado!",
            "campeao": campeao,
            "ranking_completo": ranking_formatado
        }
