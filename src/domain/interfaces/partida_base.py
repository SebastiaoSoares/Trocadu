from abc import ABC, abstractmethod
from typing import List, Deque, Optional
from collections import deque
from src.domain.entities.jogador import Jogador
from src.domain.entities.equipe import Equipe
from src.domain.entities.turno import Turno
from src.domain.interfaces.repositorio_palavras import BancoDePalavras

class GerenciadorDePartida(ABC):
    """
    Base abstrata para gerenciar o ciclo de vida e regras gerais da partida.
    """

    def __init__(self, pool_jogadores: List[Jogador], banco_palavras: BancoDePalavras):
        self._pool_jogadores: List[Jogador] = pool_jogadores
        self._banco_palavras: BancoDePalavras = banco_palavras
        self._turno_atual: Optional[Turno] = None

    def iniciar_jogo(self):
        """
        Executa o fluxo: setup, execução do modo e encerramento.
        """
        try:
            self._setup()
        except Exception as e:
            print(f"Erro na inicialização: {e}")
            return

        self._iniciar_modo()
        self._processar_vitoria()

    def _gerar_permutacoes_duplas(self) -> Deque[Equipe]:
        """
        Gera uma fila de duplas usando algoritmo Round Robin para garantir confrontos únicos.
        """
        jogadores = list(self._pool_jogadores)
        if len(jogadores) % 2 != 0:
            jogadores.append(None)

        num_rodadas = len(jogadores) - 1
        fila_partidas = deque()
        fixo = jogadores[0]
        resto = deque(jogadores[1:])

        for _ in range(num_rodadas):
            lista_atual = [fixo] + list(resto)
            for i in range(0, len(jogadores), 2):
                p1 = lista_atual[i]
                p2 = lista_atual[i+1]
                if p1 is not None and p2 is not None:
                    fila_partidas.append(Equipe(p1, p2))
            resto.rotate(1)
            
        return fila_partidas

    def _executar_rodada_ida_e_volta(self, dupla: Equipe):
        """
        Executa dois turnos para a mesma dupla, invertendo os papéis (Ida e Volta).
        """
        self._turno_atual = Turno(dupla, tempo_limite=60)
        
        palavra_ida = self._banco_palavras.get_palavra_aleatoria()
        self._turno_atual.definir_palavra(palavra_ida)
        self._turno_atual.iniciar_cronometro()
        
        self._turno_atual.trocar_funcoes()
        
        palavra_volta = self._banco_palavras.get_palavra_aleatoria()
        self._turno_atual.definir_palavra(palavra_volta)
        self._turno_atual.iniciar_cronometro()

        self._turno_atual = None

    @abstractmethod
    def _setup(self):
        """
        Realiza validações e configurações iniciais da partida.
        """
        pass

    @abstractmethod
    def _iniciar_modo(self):
        """
        Executa o loop principal da partida conforme as regras do modo específico.
        """
        pass

    @abstractmethod
    def _processar_vitoria(self):
        """
        Calcula resultados finais e exibe o encerramento.
        """
        pass