"""
Conjunto de testes para o PartidaRegistry, que é o sistema de registro de modos de jogo.
"""

import pytest
from src.domain.registry.partida_registry import PartidaRegistry


# FIXTURE DE LIMPEZA:

@pytest.fixture(autouse=True)
def limpar_registro():
    """
    Garante que o registro esteja limpo antes e depois de cada teste, 
    evitando que um teste interfira no outro por causa de registros antigos.
    """
    PartidaRegistry._modos_registrados = {}
    yield
    PartidaRegistry._modos_registrados = {}


# CLASSES FAKE PARA TESTE:

class JogoFake:
    pass

class OutroJogoFake:
    pass


# TESTES DO REGISTRY:

def test_registrar_com_sucesso():
    """
    Testa se o decorator registra a classe corretamente.
    """
    decorator = PartidaRegistry.registrar("FAKE")
    decorator(JogoFake)

    classe_obtida = PartidaRegistry.obter_classe("FAKE")
    assert classe_obtida == JogoFake

def test_registrar_duplicado_lanca_erro():
    """
    Testa se o sistema impede registrar duas classes com o mesmo nome.
    """
    decorator = PartidaRegistry.registrar("DUPLICADO")
    decorator(JogoFake)

    with pytest.raises(ValueError) as erro:
        decorator_2 = PartidaRegistry.registrar("DUPLICADO")
        decorator_2(OutroJogoFake)
    
    assert "já está registrado" in str(erro.value)

def test_obter_classe_ignora_case_e_espacos():
    """
    Testa se ' fake ', 'FAKE' e 'Fake' retornam a mesma coisa.
    """
    decorator = PartidaRegistry.registrar("TESTE")
    decorator(JogoFake)

    assert PartidaRegistry.obter_classe("teste") == JogoFake
    assert PartidaRegistry.obter_classe("  TESTE  ") == JogoFake

def test_obter_classe_inexistente():
    """
    Testa se retorna None para chaves que não existem.
    """
    assert PartidaRegistry.obter_classe("NAO_EXISTE") is None

def test_listar_modos():
    """
    Testa se lista todas as chaves registradas.
    """
    PartidaRegistry.registrar("MODO_A")(JogoFake)
    PartidaRegistry.registrar("MODO_B")(OutroJogoFake)

    lista = PartidaRegistry.listar_modos()
    
    assert "MODO_A" in lista
    assert "MODO_B" in lista
    assert len(lista) == 2