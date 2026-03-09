"""Módulo contendo o caso de uso do modo Treino Clássico."""

import random
from typing import Dict, Any, List, Optional
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.interfaces.partida_base import GerenciadorDePartida
from src.domain.entities.jogador import Jogador
from src.domain.entities.equipe import Equipe
from src.domain.entities.turno import Turno
from src.domain.entities.configuracao import ConfiguracaoDePartida

@PartidaRegistry.registrar("TREINO_CLASSICA")
class PartidaTreinoClassica(GerenciadorDePartida):
    """Gere a lógica de uma partida no modo de treino.

    Neste modo, o utilizador joga individualmente fazendo dupla com o 
    sistema (bot "Trocadu"). As rodadas são geradas infinitamente até 
    que o jogador decida encerrar a partida manualmente. Os resultados 
    não são gravados no histórico.

    Attributes:
        _jogador_usuario (Jogador): A instância que representa o utilizador humano.
        _jogador_sistema (Jogador): A instância que representa o bot do sistema.
        _equipe_treino (Equipe): A equipa fixa formada pelo utilizador e pelo bot.
        _rodadas_jogadas (int): O contador de quantas rodadas foram concluídas no treino.
    """

    def __init__(self, pool_jogadores: List[Jogador], pacote_palavras: object, configuracao: Optional[ConfiguracaoDePartida] = None):
        """Inicializa a partida de treino configurando a equipa fixa.

        Args:
            pool_jogadores (List[Jogador]): Lista de jogadores (geralmente ignorada 
                neste modo, pois a dupla é gerada internamente).
            pacote_palavras (object): A fonte de palavras instanciada para o treino.
            configuracao (ConfiguracaoDePartida, optional): Configurações de tempo 
                e limites por rodada. Se não fornecida, usa os valores padrão.
        """
        super().__init__(pool_jogadores, pacote_palavras, configuracao)
        
        self._jogador_usuario = Jogador("Você")
        self._jogador_sistema = Jogador("Trocadu")
        self._equipe_treino = Equipe(self._jogador_usuario, self._jogador_sistema)
        self._rodadas_jogadas = 0

    def _setup(self) -> None:
        """Prepara a partida de treino alterando o seu estado para em andamento."""
        self._status = self.Status.EM_ANDAMENTO

    def avancar(self) -> Dict[str, Any]:
        """Gera uma nova rodada de treino sorteando uma palavra.

        Ao contrário do modo competitivo, o treino não consome uma fila finita 
        de duplas. Ele simplesmente gera um novo turno para a mesma dupla fixa 
        sempre que invocado, até ser interrompido.

        Returns:
            Dict[str, Any]: Um dicionário contendo os dados do turno gerado 
            (palavra, tempo limite e mensagem de encorajamento) ou o resumo 
            final se a partida já estiver encerrada.
        """
        if self._status == self.Status.FINALIZADO:
             return self._processar_vitoria()
        
        if self._status != self.Status.EM_ANDAMENTO:
             return {"erro": "O treino precisa ser iniciado."}

        self._turno_atual = Turno(
            dupla=self._equipe_treino, 
            tempo_limite=self._configuracao.tempo_limite,
            palavras_disponiveis=self._configuracao.palavras_por_turno
        )
        
        palavras_disponiveis = self._pacote_palavras.obter_palavras()
        palavra_sorteada = random.choice(palavras_disponiveis)
        
        self._turno_atual.definir_palavra(palavra_sorteada.termo)
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

    def encerrar_manualmente(self) -> Dict[str, Any]:
        """Encerra a partida de treino de forma forçada a pedido do utilizador.

        Returns:
            Dict[str, Any]: O dicionário com o resumo da sessão de treino gerado 
            pelo método `_processar_vitoria`.
        """
        self._status = self.Status.FINALIZADO
        return self._processar_vitoria()

    def _processar_vitoria(self) -> Dict[str, Any]:
        """Gera o resumo final das rodadas jogadas na sessão de treino.

        Returns:
            Dict[str, Any]: Um dicionário contendo a mensagem de conclusão e 
            o total de rodadas praticadas pelo utilizador.
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