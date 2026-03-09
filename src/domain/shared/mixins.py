"""
Mixins utilitários para serialização e funcionalidades compartilhadas.
"""
from __future__ import annotations
import json
import random
from typing import Any, Dict, Deque, List, TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from src.domain.entities.equipe import Equipe

class JsonSerializavelMixin:
    """Mixin para converter objetos em JSON e vice-versa."""

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, json_str: str):
        dados = json.loads(json_str)
        return cls(**dados)

class PermutadorMixin:
    """Mixin responsável pela lógica de pareamento (Round Robin) e turnos."""

    _pool_jogadores: List[Any] 
    _pacote_palavras: Any
    _turno_atual: Any
    _configuracao: Any

    def _gerar_permutacoes_duplas(self) -> Deque[Equipe]:
        from src.domain.entities.equipe import Equipe 

        if not self._pool_jogadores:
            return deque()

        jogadores = list(self._pool_jogadores)
        if len(jogadores) % 2 != 0:
            jogadores.append(None)

        num_rodadas = len(jogadores) - 1
        fila_partidas: Deque[Equipe] = deque()
        
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

    def _executar_rodada_ida_e_volta(self, dupla: Equipe) -> None:
        """Configura o turno injetando os limites definidos nas configurações."""
        from src.domain.entities.turno import Turno

        self._turno_atual = Turno(
            dupla=dupla, 
            tempo_limite=self._configuracao.tempo_limite,
            palavras_disponiveis=self._configuracao.palavras_por_turno
        )
        
        palavras_disponiveis = self._pacote_palavras.obter_palavras()
        palavra_sorteada = random.choice(palavras_disponiveis)
        
        self._turno_atual.definir_palavra(palavra_sorteada.termo)
        self._turno_atual.iniciar_cronometro()