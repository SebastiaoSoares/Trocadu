"""
Conjunto de testes para os casos de uso do sistema, garantindo que as funcionalidades principais estejam funcionando conforme o esperado.
"""

import pytest
from enum import Enum
from unittest.mock import MagicMock
from src.domain.entities.jogador import Jogador
from src.domain.use_cases.partida_competitiva_classica import PartidaCompetitivaClassica
from src.domain.use_cases.partida_treino_classica import PartidaTreinoClassica


# CLASSES FAKE PARA TESTE:

class FakeUsuario:
    """
    Simula um usuário apenas com o nickname para o teste passar.
    """
    def __init__(self, nickname):
        self.nickname = nickname

class MockStatus(Enum):
    """
    Simula o Enum de Status da classe base.
    """
    AGUARDANDO = "AGUARDANDO"
    EM_ANDAMENTO = "EM_ANDAMENTO"
    FINALIZADO = "FINALIZADO"

class MockBancoPalavras:
    """
    Simula o banco de dados retornando sempre a mesma palavra.
    """
    def get_palavra_aleatoria(self):
        return "PYTHON"


# FIXTURES (Dados prontos para usar nos testes):

@pytest.fixture
def banco_mock():
    return MockBancoPalavras()

@pytest.fixture
def pool_jogadores():
    return [
        Jogador("Aisha"),
        Jogador("Ramom"),
        Jogador("Sabrina"),
        Jogador("Sebastião")
    ]


# TESTES DE PARTIDA COMPETITIVA CLÁSSICA:

def test_competitiva_setup_inicial(pool_jogadores, banco_mock):
    """
    Verifica se o jogo cria o ranking zerado e gera a fila de partidas.
    """
    jogo = PartidaCompetitivaClassica(pool_jogadores, banco_mock)
    
    jogo.Status = MockStatus 
    
    jogo._setup()
    
    assert len(jogo._ranking) == 4
    assert jogo._ranking["Aisha"] == 0
    
    assert len(jogo._fila_de_duplas) > 0

def test_competitiva_pontuacao(pool_jogadores, banco_mock):
    """
    Verifica se computar pontos atualiza o ranking corretamente.
    """
    jogo = PartidaCompetitivaClassica(pool_jogadores, banco_mock)
    jogo.Status = MockStatus
    jogo._setup()
    jogo._status = MockStatus.EM_ANDAMENTO

    resultado = jogo.avancar()
    nome_j1 = resultado["dupla"]["jogador1"]
    nome_j2 = resultado["dupla"]["jogador2"]

    jogo.computar_pontos_rodada(10)

    assert jogo._ranking[nome_j1] == 10
    assert jogo._ranking[nome_j2] == 10

    for nome, pontos in jogo._ranking.items():
        if nome not in [nome_j1, nome_j2]:
            assert pontos == 0

def test_competitiva_fim_de_jogo(pool_jogadores, banco_mock):
    """
    Verifica se o jogo encerra e retorna o campeão quando a fila acaba.
    """
    jogo = PartidaCompetitivaClassica(pool_jogadores, banco_mock)
    jogo.Status = MockStatus
    jogo._setup()
    jogo._status = MockStatus.EM_ANDAMENTO

    jogo._fila_de_duplas.clear()

    jogo._ranking["Aisha"] = 50
    jogo._ranking["Ramom"] = 20

    resultado = jogo.avancar()

    assert resultado["status"] == "FINALIZADO"
    assert resultado["dados"]["campeao"]["nome"] == "Aisha"
    assert jogo._status == MockStatus.FINALIZADO


# TESTES DE PARTIDA TREINO CLÁSSICA:

def test_treino_inicializacao(banco_mock):
    """
    Verifica se cria os jogadores virtuais (Você vs Trocadu).
    """
    jogo = PartidaTreinoClassica([], banco_mock)

    assert jogo._jogador_usuario.nome == "Você"
    assert jogo._jogador_sistema.nome == "Trocadu"

def test_treino_fluxo(banco_mock):
    """
    Verifica se o jogo avança infinitamente e conta as rodadas.
    """
    jogo = PartidaTreinoClassica([], banco_mock)
    jogo.Status = MockStatus
    jogo._setup()
    
    for i in range(1, 4):
        res = jogo.avancar()
        assert res["status"] == "RODADA_NOVA"
        assert res["palavra"] == "PYTHON"
        assert jogo._rodadas_jogadas == i

def test_treino_encerrar_manual(banco_mock):
    """
    Verifica se o botão de encerrar funciona.
    """
    jogo = PartidaTreinoClassica([], banco_mock)
    jogo.Status = MockStatus
    jogo._setup()
    
    res = jogo.encerrar_manualmente()
    
    assert res["status"] == MockStatus.FINALIZADO.value
    assert "Treino concluído" in res["mensagem"]