"""
Conjunto de testes para a PartidaFactory, que é a fábrica responsável por criar instâncias dos modos de jogo.
"""

import pytest
from src.domain.shared.factories import PartidaFactory
from src.domain.registry.partida_registry import PartidaRegistry
from src.domain.entities.jogador import Jogador


# CLASSES FAKE PARA TESTE:

class FakeGerenciadorPartida:
    """
    Classe Fake que simula um modo de jogo concreto.
    """
    def __init__(self, pool_jogadores, banco_palavras):
        self.pool_jogadores = pool_jogadores
        self.banco_palavras = banco_palavras


# FIXTURES (Dados prontos para usar nos testes):

@pytest.fixture(autouse=True)
def setup_registry():
    """
    Limpa o registro e cadastra nosso Jogo Fake para a fábrica poder achar.
    """
    PartidaRegistry._modos_registrados = {}
    
    PartidaRegistry.registrar("TEST_MODE")(FakeGerenciadorPartida)
    
    yield
    PartidaRegistry._modos_registrados = {}

@pytest.fixture
def mock_dados():
    """
    Retorna dados fictícios para criar a partida.
    """
    jogadores = [Jogador(None), Jogador(None)]
    banco = "BancoDePalavrasMock"
    return jogadores, banco


# TESTES DA FACTORY:

def test_factory_criar_partida_existente(mock_dados):
    """
    Testa se a Factory instancia a classe correta quando o modo existe.
    """
    jogadores, banco = mock_dados
    
    jogo = PartidaFactory.criar_partida("TEST_MODE", jogadores, banco)
    
    assert isinstance(jogo, FakeGerenciadorPartida)
    assert jogo.pool_jogadores == jogadores
    assert jogo.banco_palavras == banco

def test_factory_erro_modo_invalido(mock_dados):
    """
    Testa se a Factory avisa quando pedimos um modo que não existe.
    """
    jogadores, banco = mock_dados
    
    with pytest.raises(ValueError) as erro:
        PartidaFactory.criar_partida("NAO_EXISTE", jogadores, banco)
    
    assert "inválido" in str(erro.value)