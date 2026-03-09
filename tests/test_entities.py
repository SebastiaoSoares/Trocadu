"""
Conjunto de testes para as entidades do sistema, garantindo que as classes e seus métodos estejam funcionando corretamente.
"""

import pytest
from uuid import uuid4
from src.domain.entities.usuario import Usuario
from src.domain.entities.jogador import Jogador
from src.domain.entities.equipe import Equipe
from src.domain.entities.palavra import Palavra
from src.domain.entities.turno import Turno
from src.domain.entities.placar import Placar


# FIXTURES (Dados prontos para usar nos testes):

@pytest.fixture
def usuario_teste():
    """
    Cria um usuário padrão para os testes.
    """
    return Usuario(uuid4(), "NickTeste")

@pytest.fixture
def jogador_teste(usuario_teste):
    """
    Cria um jogador vinculado ao usuário padrão.
    """
    return Jogador(usuario_teste)

@pytest.fixture
def equipe_teste():
    """
    Cria uma equipe com 2 jogadores.
    """
    j1 = Jogador("j1")
    j2 = Jogador("j2")
    return Equipe(j1, j2)


# TESTES DE USUÁRIO

def test_usuario_criar(usuario_teste):
    """
    Testa se o __init__ define os atributos corretamente.
    """
    assert usuario_teste.nickname == "NickTeste"
    assert usuario_teste.id is not None

def test_usuario_atualizar_perfil(usuario_teste):
    """
    Testa a função atualizar_perfil.
    """
    usuario_teste.atualizar_perfil("NovoNick")
    assert usuario_teste.nickname == "NovoNick"

def test_usuario_to_json(usuario_teste):
    """
    Testa a conversão para JSON (dicionário).
    """
    dados = usuario_teste.to_json()
    assert dados['nickname'] == "NickTeste"
    assert 'id' in dados


# TESTES DE JOGADOR:

def test_jogador_inicializar(jogador_teste):
    """
    Testa se o jogador começa com 0 pontos.
    """
    assert jogador_teste.pontuacao_individual == 0

def test_jogador_incrementar_pontos(jogador_teste):
    """
    Testa a função incrementar_pontos.
    """
    jogador_teste.incrementar_pontos(10)
    assert jogador_teste.pontuacao_individual == 10
    jogador_teste.incrementar_pontos(5)
    assert jogador_teste.pontuacao_individual == 15


# TESTES DE EQUIPE:

def test_equipe_inicializar(equipe_teste):
    """
    Testa se a equipe inicia com pontuação zerada.
    """
    assert equipe_teste.pontuacao_da_dupla == 0

def test_equipe_registrar_pontos_rodada(equipe_teste):
    """
    Testa registrar_pontos_rodada.
    Deve somar na equipe E nos dois jogadores individualmente.
    """
    equipe_teste.registrar_pontos_rodada(100)

    assert equipe_teste.pontuacao_da_dupla == 100
    
    assert equipe_teste.jogador_1.pontuacao_individual == 100
    assert equipe_teste.jogador_2.pontuacao_individual == 100

def test_equipe_to_json(equipe_teste):
    """
    Testa a conversão para JSON da equipe.
    """
    equipe_teste.registrar_pontos_rodada(50)
    dados = equipe_teste.to_json()
    
    assert dados['pontuacao'] == 50
    assert dados['jogador_1'] == "j1"
    assert dados['jogador_2'] == "j2"


# TESTES DE PALAVRA:

def test_palavra_propriedades():
    """
    Testa getters e setters da Palavra.
    """
    p = Palavra("Café", "Bebida quente", "Alimentos")
    assert p.termo == "Café"
    assert p.dica == "Bebida quente"
    assert p.categoria == "Alimentos"

def test_palavra_str():
    """
    Testa a conversão para string.
    """
    p = Palavra("Python", categoria="Linguagens de Programação")
    assert str(p) == "Python (Linguagens de Programação)"

def test_palavra_to_dict():
    """
    Testa o to_dict.
    """
    p = Palavra("Rato", categoria="Animais")
    d = p.to_dict()
    assert d['termo'] == "Rato"
    assert d['categoria'] == "Animais"


# TESTES DE TURNO:

def test_turno_inicializar(equipe_teste):
    """
    Testa se o turno define guia e adivinhador corretamente.
    """
    turno = Turno(equipe_teste)
    assert turno.guia_atual == equipe_teste.jogador_1
    assert turno.adivinhador_atual == equipe_teste.jogador_2

def test_turno_definir_palavra(equipe_teste):
    """
    Testa se a palavra é definida corretamente.
    """
    turno = Turno(equipe_teste)
    turno.definir_palavra("Rato")
    assert turno.palavra_atual == "Rato"

def test_turno_trocar_funcoes(equipe_teste, capsys):
    """
    Testa se a troca de Guia/Adivinhador funciona.
    """
    turno = Turno(equipe_teste)
    guia_original = turno.guia_atual
    adivinhador_original = turno.adivinhador_atual

    turno.trocar_funcoes()

    assert turno.guia_atual == adivinhador_original
    assert turno.adivinhador_atual == guia_original


# TESTES DE PLACAR:

def test_placar_processar_ranking_ordem_correta():
    """
    Testa se o método estático ordena corretamente os pontos e gera os metadados (posição).
    """

    ranking_bruto = {
        "Nick01": 10,
        "Nick02": 100,
        "Nick03": 50
    }

    resultado = Placar.processar_ranking(ranking_bruto)

    assert len(resultado) == 3
    
    # 1º Lugar
    assert resultado[0]["posicao"] == 1
    assert resultado[0]["nome"] == "Nick02"
    assert resultado[0]["pontos"] == 100
    
    # 2º Lugar
    assert resultado[1]["posicao"] == 2
    assert resultado[1]["nome"] == "Nick03"
    assert resultado[1]["pontos"] == 50
    
    # 3º Lugar
    assert resultado[2]["posicao"] == 3
    assert resultado[2]["nome"] == "Nick01"
    assert resultado[2]["pontos"] == 10

def test_placar_obter_campeao():
    """
    Testa se a lógica de extração do campeão retorna o primeiro da lista.
    """
    ranking_processado = [
        {"posicao": 1, "nome": "Vencedor", "pontos": 999},
        {"posicao": 2, "nome": "Vice", "pontos": 500}
    ]
    
    campeao = Placar.obter_campeao(ranking_processado)
    
    assert campeao is not None
    assert campeao["nome"] == "Vencedor"
    assert campeao["pontos"] == 999

def test_placar_vazio():
    """
    Testa comportamento com dicionário vazio (sem jogadores).
    """
    ranking_bruto = {}
    
    resultado = Placar.processar_ranking(ranking_bruto)
    campeao = Placar.obter_campeao(resultado)
    
    assert resultado == []
    assert campeao is None
