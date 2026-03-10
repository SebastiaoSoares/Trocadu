"""Módulo contendo mixins utilitários para serialização e funcionalidades partilhadas."""

from __future__ import annotations
import json
import random
from typing import Any, Dict, Deque, List, TYPE_CHECKING
from collections import deque

if TYPE_CHECKING:
    from src.domain.entities.equipe import Equipe

class JsonSerializavelMixin:
    """Mixin para converter objetos em dicionários e JSON, e vice-versa.

    Providencia métodos utilitários para facilitar a serialização das 
    entidades de domínio que precisem de ser trafegadas via API ou guardadas.
    """

    def to_dict(self) -> Dict[str, Any]:
        """Converte as propriedades do objeto num dicionário.

        Returns:
            Dict[str, Any]: Um dicionário representando os atributos internos do objeto.
        """
        return self.__dict__

    def to_json(self) -> str:
        """Converte o objeto numa string no formato JSON.

        Returns:
            str: Representação do objeto em formato JSON, formatada com indentação.
        """
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=4)

    @classmethod
    def from_json(cls, json_str: str) -> Any:
        """Cria uma instância da classe a partir de uma string JSON.

        Args:
            json_str (str): A string contendo os dados do objeto em formato JSON.

        Returns:
            Any: Uma nova instância da classe preenchida com os dados do JSON.
        """
        dados = json.loads(json_str)
        return cls(**dados)

class PermutadorMixin:
    """Mixin responsável pela lógica de emparelhamento (Round Robin) e turnos.

    Pode ser injetado em classes gestoras de partida para herdar 
    comportamentos complexos de rotação de jogadores (Todos contra Todos) 
    sem criar uma árvore de herança rígida.

    Attributes:
        _pool_jogadores (List[Any]): Lista de jogadores disponíveis na partida.
        _pacote_palavras (Any): Fonte de palavras injetada na partida.
        _turno_atual (Any): O turno (rodada) ativo no momento.
        _configuracao (Any): Configurações de tempo e limite de palavras do jogo.
    """

    _pool_jogadores: List[Any] 
    _pacote_palavras: Any
    _turno_atual: Any
    _configuracao: Any

    def _gerar_permutacoes_duplas(self) -> Deque[Equipe]:
        """Gera a fila de duplas utilizando o algoritmo Round Robin.

        Garante que cada jogador faça dupla com todos os outros participantes 
        exatamente uma vez. Se o número de jogadores for ímpar, o algoritmo 
        adiciona temporariamente um jogador "fantasma" (`None`) para 
        equilibrar a rotação, filtrando-o no momento da criação das equipas.

        Returns:
            Deque[Equipe]: Uma fila (deque) contendo as instâncias de `Equipe`
            já formadas e prontas para as rodadas.
        """
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
        """Configura o turno injetando os limites definidos nas configurações.

        Cria uma nova instância de `Turno` para a dupla fornecida, sorteia a 
        primeira palavra a partir do repositório de palavras e inicia o cronómetro
        baseando-se nos limites configurados na partida.

        Args:
            dupla (Equipe): A dupla (equipa) que atuará no turno atual.
        """
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