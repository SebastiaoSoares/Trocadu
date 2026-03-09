"""Módulo contendo o contrato base para o gestor de partidas."""

from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, List, Optional
from collections import deque
from src.domain.entities.jogador import Jogador
from src.domain.entities.turno import Turno
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras
from src.domain.entities.configuracao import ConfiguracaoDePartida

class GerenciadorDePartida(ABC):
    """Base abstrata para gerir o ciclo de vida e as regras gerais da partida.

    Esta classe implementa o padrão Template Method, definindo o esqueleto 
    do algoritmo de jogo através do método `iniciar_jogo` e obrigando as 
    subclasses a implementarem os detalhes específicos em `_setup`, `avancar` 
    e `_processar_vitoria`.

    Attributes:
        _pool_jogadores (List[Jogador]): A lista de jogadores inscritos na partida.
        _pacote_palavras (PacoteDePalavras): A fonte de palavras que será utilizada.
        _configuracao (ConfiguracaoDePartida): Os limites e regras de tempo/palavras.
        _turno_atual (Turno | None): O turno que está a decorrer no momento.
        _status (GerenciadorDePartida.Status): O estado atual em que a partida se encontra.
    """

    class Status(Enum):
        """Enumeração que representa os estados possíveis de uma partida."""
        NAO_INICIADO = "Não Iniciado"
        EM_ANDAMENTO = "Em Andamento"
        FINALIZADO = "Finalizado"

    def __init__(
        self, 
        pool_jogadores: List[Jogador], 
        pacote_palavras: PacoteDePalavras,
        configuracao: Optional[ConfiguracaoDePartida] = None
    ):
        """Inicializa as dependências e o estado base do gestor de partida.

        Args:
            pool_jogadores (List[Jogador]): Lista com os participantes do jogo.
            pacote_palavras (PacoteDePalavras): Interface para obtenção das palavras.
            configuracao (ConfiguracaoDePartida, optional): Configurações da partida.
                Se não for fornecida, será instanciada uma configuração padrão.
        """
        self._pool_jogadores: List[Jogador] = pool_jogadores
        self._pacote_palavras: PacoteDePalavras = pacote_palavras
        
        self._configuracao: ConfiguracaoDePartida = configuracao or ConfiguracaoDePartida()
        
        self._turno_atual: Optional[Turno] = None
        self._status: GerenciadorDePartida.Status = self.Status.NAO_INICIADO

    def iniciar_jogo(self) -> Dict[str, Any]:
        """Inicia o jogo e prepara a partida.

        Este método orquestra a chamada ao método abstrato `_setup` e altera 
        o estado da partida para `EM_ANDAMENTO`.

        Returns:
            Dict[str, Any]: Um dicionário contendo a mensagem de sucesso e o 
            status atual, ou uma mensagem de erro em caso de falha.
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
    def _setup(self) -> None:
        """Realiza validações e configurações iniciais da partida.
        
        Deve ser implementado pelas subclasses para preparar estruturas 
        específicas (como filas de duplas ou rankings) antes do início do jogo.
        """
        pass

    @abstractmethod
    def avancar(self) -> Dict[str, Any]:
        """Executa um único passo (rodada) ou finaliza o jogo.

        Deve ser implementado pelas subclasses para ditar o que acontece 
        quando o jogo transita para a próxima fase ou turno.

        Returns:
            Dict[str, Any]: O estado atualizado da rodada, a palavra sorteada, 
            os jogadores ativos ou o resultado final caso a partida termine.
        """
        pass

    @abstractmethod
    def _processar_vitoria(self) -> Any:
        """Calcula os resultados finais e exibe o encerramento.

        Deve ser implementado pelas subclasses para definir a lógica de 
        vitória, formatação de placar e persistência de dados.
        """
        pass