from typing import Dict, Any, List
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.entities.jogador import Jogador
from src.domain.entities.equipe import Equipe
from src.domain.entities.turno import Turno

class PartidaTreinoClassica(GerenciadorDePartida):
    """
    Modo Treino:
    - Jogador Único (Você) + Sistema (Trocadu).
    - Loop infinito de palavras aleatórias.
    - Sem ranking, sem vencedores.
    - Termina apenas quando solicitado explicitamente.
    """

    def __init__(self, pool_jogadores: List[Jogador], banco_palavras: object):
        super().__init__(pool_jogadores, banco_palavras)
        
        self._jogador_usuario = Jogador(nome="Você")
        self._jogador_sistema = Jogador(nome="Trocadu")
        
        self._equipe_treino = Equipe(self._jogador_usuario, self._jogador_sistema)
        
        self._rodadas_jogadas = 0

    def _setup(self):
        """
        No treino, o setup é apenas garantir que o jogo está 'pronto'.
        Não geramos fila de permutações.
        """

        self._status = self.Status.EM_ANDAMENTO

    def avancar(self) -> Dict[str, Any]:
        """
        Gera uma nova rodada aleatória eternamente, até que o status mude.
        """

        if self._status == self.Status.FINALIZADO:
             return self._processar_vitoria()
        
        if self._status != self.Status.EM_ANDAMENTO:
             return {"erro": "O treino precisa ser iniciado."}

        self._turno_atual = Turno(self._equipe_treino, tempo_limite=90)
        
        palavra = self._banco_palavras.get_palavra_aleatoria()
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
        """
        Método específico para o botão 'Encerrar' do Frontend.
        """
        self._status = self.Status.FINALIZADO
        return self._processar_vitoria()

    def _processar_vitoria(self):
        """
        Retorna apenas um feedback amigável de quanto o usuário treinou.
        """
        self._status = self.Status.FINALIZADO
        
        return {
            "status": self.Status.FINALIZADO.value,
            "mensagem": "Treino concluído!",
            "resumo": {
                "total_rodadas": self._rodadas_jogadas,
                "feedback": "Parabéns! Continue praticando para o modo competitivo."
            }
        }