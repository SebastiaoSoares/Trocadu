from typing import Dict, Any, List, Optional
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.entities.jogador import Jogador
from src.domain.entities.equipe import Equipe
from src.domain.entities.turno import Turno
from src.domain.entities.configuracao import ConfiguracaoDePartida

@PartidaRegistry.registrar("TREINO_CLASSICA")
class PartidaTreinoClassica(GerenciadorDePartida):

    def __init__(self, pool_jogadores: List[Jogador], pacote_palavras: object, configuracao: Optional[ConfiguracaoDePartida] = None):
        super().__init__(pool_jogadores, pacote_palavras, configuracao)
        
        self._jogador_usuario = Jogador("Você")
        self._jogador_sistema = Jogador("Trocadu")
        self._equipe_treino = Equipe(self._jogador_usuario, self._jogador_sistema)
        self._rodadas_jogadas = 0

    def _setup(self):
        self._status = self.Status.EM_ANDAMENTO

    def avancar(self) -> Dict[str, Any]:
        if self._status == self.Status.FINALIZADO:
             return self._processar_vitoria()
        
        if self._status != self.Status.EM_ANDAMENTO:
             return {"erro": "O treino precisa ser iniciado."}

        self._turno_atual = Turno(
            dupla=self._equipe_treino, 
            tempo_limite=self._configuracao.tempo_limite,
            saltos_disponiveis=self._configuracao.limite_saltos
        )
        
        palavra = self._pacote_palavras.get_palavra_aleatoria()
        self._turno_atual.definir_palavra(palavra)
        self._turno_atual.iniciar_cronometro()

        self._rodadas_jogadas += 1

        return {
            "status": "RODADA_NOVA",
            "modo": "TREINO",
            "dupla": {
                "jogador1": self._jogador_usuario.nome,
                "jogador2": self._jogador_sistema.nome
            },
            "palavra": self._turno_atual.palavra_atual,
            "tempo_limite": self._turno_atual.tempo_limite,
            "mensagem": "Treine à vontade! Clique em 'Encerrar' para parar."
        }

    def encerrar_manualmente(self):
        self._status = self.Status.FINALIZADO
        return self._processar_vitoria()

    def _processar_vitoria(self):
        self._status = self.Status.FINALIZADO
        return {
            "status": self.Status.FINALIZADO.value,
            "mensagem": "Treino concluído!",
            "resumo": {
                "total_rodadas": self._rodadas_jogadas,
                "feedback": "Parabéns! Continue praticando para o modo competitivo."
            }
        }