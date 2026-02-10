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
    Cria uma equipe completa com 2 jogadores.
    """
    u1 = Usuario(uuid4(), "PlayerOne")
    u2 = Usuario(uuid4(), "PlayerTwo")
    j1 = Jogador(u1)
    j2 = Jogador(u2)
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

def test_jogador_obter_nome(jogador_teste):
    """
    Testa se obter_nome busca do usuário vinculado.
    """
    assert jogador_teste.obter_nome() == "NickTeste"


# TESTES DE EQUIPE:

def test_equipe_inicializar(equipe_teste):
    """
    Testa se a equipe inicia com pontuação zerada.
    """
    assert equipe_teste.pontuacao_da_dupla == 0
    assert equipe_teste.jogador_1.obter_nome() == "PlayerOne"

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
    assert dados['jogador_1'] == "PlayerOne"
    assert dados['jogador_2'] == "PlayerTwo"


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

def test_turno_validar_chute(equipe_teste, capsys):
    """
    Testa a lógica de acerto e erro do chute.
    """
    turno = Turno(equipe_teste)
    turno.definir_palavra("Python")

    assert turno.validar_chute("Java") is False
    
    assert turno.validar_chute("python") is True
    assert turno.validar_chute("PYTHON ") is True

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

def test_placar_ranking_individual(capsys):
    """
    Testa se o placar ordena os jogadores corretamente.
    """
    j1 = Jogador(Usuario(uuid4(), "Nick01"))
    j1.incrementar_pontos(10)
    
    j2 = Jogador(Usuario(uuid4(), "Nick02"))
    j2.incrementar_pontos(100)
    
    j3 = Jogador(Usuario(uuid4(), "Nick03"))
    j3.incrementar_pontos(50)

    placar = Placar()
    ranking = placar.exibir_ranking_individual([j1, j2, j3])

    assert ranking["Nick02"] == 100
    assert ranking["Nick03"] == 50
    assert ranking["Nick01"] == 10

    out, _ = capsys.readouterr()
    assert "1º Lugar: Nick02" in out
    assert "2º Lugar: Nick03" in out
    assert "3º Lugar: Nick01" in out