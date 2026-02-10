"""
Conjunto de testes para os Mixins do projeto.
"""

import pytest
import json
from collections import deque
from src.domain.shared.mixins import PermutadorMixin, JsonSerializavelMixin


# CLASSES FAKE PARA TESTE:

class FakePermutador(PermutadorMixin):
    """
    Classe que finge ser o jogo para testar o sorteio.
    """
    def __init__(self, lista_jogadores):
        self._pool_jogadores = lista_jogadores
        self._banco_palavras = None 
        self._turno_atual = None

class FakeObjetoJson(JsonSerializavelMixin):
    """
    Classe simples para testar o JSON.
    """
    def __init__(self, nome, nivel):
        self.nome = nome
        self.nivel = nivel


# TESTES DO PERMUTADOR:

def test_permutacao_numero_par():
    """
    Testa se gera as partidas corretamente com 4 jogadores (par).
    """
    jogadores = ["Aisha", "Ramom", "Sabrina", "Sebastião"]
    permutador = FakePermutador(jogadores)
    
    fila = permutador._gerar_permutacoes_duplas()
    
    assert len(fila) > 0
    
    primeira_partida = fila[0]
    
    assert primeira_partida.jogador_1 in jogadores
    assert primeira_partida.jogador_2 in jogadores

def test_permutacao_numero_impar():
    """
    Testa se lida com número ímpar (3 jogadores).
    """
    jogadores = ["Ramom", "Sabrina", "Sebastião"]
    permutador = FakePermutador(jogadores)
    
    fila = permutador._gerar_permutacoes_duplas()
    
    assert len(fila) > 0

def test_permutacao_lista_vazia():
    """
    Testa se não quebra com lista vazia.
    """
    permutador = FakePermutador([])
    fila = permutador._gerar_permutacoes_duplas()
    assert len(fila) == 0


# TESTES DO JSON:

def test_to_json_formato():
    """
    Testa se cria a string JSON certa.
    """
    obj = FakeObjetoJson("Teste", 10)
    json_str = obj.to_json()
    
    assert isinstance(json_str, str)
    assert "Teste" in json_str
    assert "10" in json_str

def test_from_json_recriacao():
    """
    Testa se recria o objeto a partir do texto.
    """
    json_entrada = '{"nome": "Recriado", "nivel": 99}'
    
    novo = FakeObjetoJson.from_json(json_entrada)
    
    assert isinstance(novo, FakeObjetoJson)
    assert novo.nome == "Recriado"
    assert novo.nivel == 99