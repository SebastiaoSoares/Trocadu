from src.domain.entities.placar import Placar
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.shared.mixins import PermutadorMixin
from src.domain.entities.configuracao import ConfiguracaoDePartida
from typing import Any, Dict, Optional

@PartidaRegistry.registrar("COMPETITIVA_CLASSICA")
class PartidaCompetitivaClassica(PermutadorMixin, GerenciadorDePartida):

    def __init__(self, pool_jogadores: list, pacote_palavras: object, configuracao: Optional[ConfiguracaoDePartida] = None):
        super().__init__(pool_jogadores, pacote_palavras, configuracao)
        self._ranking: Dict[str, int] = {}
        self._dupla_atual = None
        self._fase_rodada = None

    def _setup(self):
        self._fila_de_duplas = self._gerar_permutacoes_duplas()
        self._ranking = {jogador.nome: 0 for jogador in self._pool_jogadores}

    def computar_pontos_rodada(self, pontos_conquistados: int):
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

        if self._dupla_atual is None or self._fase_rodada == "volta":
            if not self._fila_de_duplas:
                self._status = self.Status.FINALIZADO
                resultado_final = self._processar_vitoria()
                return {
                    "status": "FINALIZADO",
                    "dados": resultado_final
                }

            self._dupla_atual = self._fila_de_duplas.popleft()
            self._fase_rodada = "ida"
            self._executar_rodada_ida_e_volta(self._dupla_atual)
            
        else:
            self._fase_rodada = "volta"
            self._executar_rodada_ida_e_volta(self._dupla_atual)
            
            self._turno_atual.trocar_funcoes()

        return {
            "status": "RODADA_NOVA",
            "fase": self._fase_rodada,
            "dupla": {
                "guia": self._turno_atual.guia_atual.nome,
                "adivinhador": self._turno_atual.adivinhador_atual.nome
            },
            "palavra": self._turno_atual.palavra_atual,
            "tempo_limite": self._turno_atual.tempo_limite,
            "saltos_disponiveis": self._turno_atual.saltos_disponiveis
        }

    def _processar_vitoria(self):
        self._status = self.Status.FINALIZADO
        ranking_formatado = Placar.processar_ranking(self._ranking)
        campeao = Placar.obter_campeao(ranking_formatado)

        return {
            "mensagem": "Torneio encerrado!",
            "campeao": campeao,
            "ranking_completo": ranking_formatado
        }
