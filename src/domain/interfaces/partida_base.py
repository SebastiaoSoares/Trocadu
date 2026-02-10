from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from collections import deque
from src.domain.entities.jogador import Jogador
from src.domain.entities.turno import Turno
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras

class GerenciadorDePartida(ABC):
    """
    Base abstrata para gerenciar o ciclo de vida e regras gerais da partida.
    """

    class Status(Enum):
        NAO_INICIADO = "Não Iniciado"
        EM_ANDAMENTO = "Em Andamento"
        FINALIZADO = "Finalizado"

    def __init__(self, pool_jogadores: List[Jogador], pacote_palavras: PacoteDePalavras):
        self._pool_jogadores: List[Jogador] = pool_jogadores
        self._pacote_palavras: PacoteDePalavras = pacote_palavras
        self._turno_atual: Optional[Turno] = None
        self._status: GerenciadorDePartida.Status = self.Status.NAO_INICIADO

    def iniciar_jogo(self) -> Dict[str, Any]:
        """
        Inicia o jogo e prepara a partida (setup), mas deixa a responsabilidade
        de gerenciar o avanço do jogo com a classe filha.
        """
        try:
            self._setup()
            self._status = self.Status.EM_ANDAMENTO
            return {
                "mensagem": "Partida iniciada com sucesso.",
                "status": self._status.value
            }
        except Exception as e:
            return {"erro": f"Falha ao iniciar: {str(e)}"}

    @abstractmethod
    def _setup(self):
        """
        Realiza validações e configurações iniciais da partida.
        """
        pass

    @abstractmethod
    def avancar(self) -> Dict[str, Any]:
        """
        Executa um único passo (rodada) ou finaliza o jogo.
        """
        pass

    @abstractmethod
    def _processar_vitoria(self):
        """
        Calcula resultados finais e exibe o encerramento.
        """
        pass