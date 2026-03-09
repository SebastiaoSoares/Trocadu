# Trocadu

Trocadu é um Party Game desenvolvido como uma API RESTful, baseando-se no paradígma da Programação Orientada a Objetos (POO).


## Instalação

Faça clone do projeto:
```bash
git clone https://github.com/SebastiaoSoares/Trocadu.git
```


## Diagrama de Classes

```mermaid
classDiagram
    class PacoteDePalavras {
        <<Interface>>
        +obter_palavras()* List~Palavra~
    }
    
    class PacoteArquivo {
        -caminho_arquivo: str
        +obter_palavras() List~Palavra~
    }

    class PacotePersonalizado {
        -id_usuario: uuid
        +obter_palavras() List~Palavra~
    }
    
    PacoteDePalavras <|-- PacoteArquivo
    PacoteDePalavras <|-- PacotePersonalizado

    class JsonSerializavelMixin {
        <<Mixin>>
        +to_json() str
        +to_dict() dict
    }

    class PermutadorMixin {
        <<Mixin>>
        #gerar_permutacoes_duplas() Deque~Equipe~
        #executar_rodada_ida_e_volta(dupla: Equipe)
    }

    class Usuario {
        -id: uuid
        -nickname: str
        +atualizar_perfil()
    }

    class Jogador {
        -usuario_ref: Usuario
        -pontuacao_individual: int
        +incrementar_pontos(qtd: int)
        +obter_nome() str
    }

    class Equipe {
        <<Transient>> 
        -jogador_1: Jogador
        -jogador_2: Jogador
        -pontuacao_da_dupla: int
        +registrar_pontos_rodada(pontos: int)
    }

    class Placar {
        <<Service>>
        +processar_ranking(dados: dict)$ List~dict~
        +obter_campeao(lista: list)$ dict
    }
    
    class Palavra {
        -termo: str
        -dica: str
        -categoria: str
        +termo() str
        +dica() str
    }

    JsonSerializavelMixin <|-- Usuario
    JsonSerializavelMixin <|-- Equipe
    JsonSerializavelMixin <|-- Palavra

    Equipe o-- Jogador : "Agrupa"
    Jogador --> Usuario : "Refere-se"

    class GerenciadorDePartida {
        <<Abstract>>
        #pool_jogadores: List~Jogador~
        #turno_atual: Turno
        #pacote_palavras: PacoteDePalavras
        +iniciar_jogo() final
        #setup()*
        #avancar()*
        #processar_vitoria()*
    }

    class PartidaCompetitivaClassica {
        -ranking: dict
        -fila_de_duplas: deque
        #setup()
        +avancar()
        +computar_pontos_rodada(pontos: int)
        #processar_vitoria()
    }

    class PartidaTreinoClassica {
        -jogador_usuario: Jogador
        -jogador_sistema: Jogador
        #setup()
        +avancar()
        +encerrar_manualmente()
        #processar_vitoria()
    }
    
    class PartidaRegistry {
        <<Singleton>>
        +registrar(chave: str)
        +obter_classe(chave: str) Type
    }

    GerenciadorDePartida <|-- PartidaCompetitivaClassica
    GerenciadorDePartida <|-- PartidaTreinoClassica
    
    PermutadorMixin <|-- PartidaCompetitivaClassica : "Herança Múltipla"

    PartidaCompetitivaClassica ..> Placar : "Usa para ordenar"
    GerenciadorDePartida *-- Turno
    GerenciadorDePartida --> PacoteDePalavras : "Consome"

    class Turno {
        -dupla: Equipe
        -palavra_atual: str
        -tempo_limite: int
        -palavras_por_turno: int
        +definir_palavra(str)
        +iniciar_cronometro()
        +consumir_palavra() bool
        +trocar_funcoes() dict
    }

    Turno --> Equipe
    
    class PartidaFactory {
        <<Factory>>
        +criar_partida(tipo: str, pool: List~Jogador~, banco: object) GerenciadorDePartida
    }

    PartidaFactory ..> PartidaRegistry : "Consulta"
    PartidaFactory ..> GerenciadorDePartida : "Cria"
```


## Definição da Estrutura de Pastas

```
Trocadu/
├── src/
│   ├── domain/                             
│   │   ├── __init__.py
│   │   │
│   │   ├── entities/                       # Entidades (SRP)
│   │   │   ├── __init__.py
│   │   │   ├── jogador.py
│   │   │   ├── equipe.py
│   │   │   ├── turno.py
│   │   │   ├── placar.py
│   │   │   └── palavra.py
│   │   │
│   │   ├── interfaces/                     # Contratos (DIP)
│   │   │   ├── __init__.py
│   │   │   ├── partida_base.py             # Classe Abstrata (Template Method)
│   │   │   └── repositorio_palavras.py     # Interface para fontes de dados
│   │   │
│   │   ├── use_cases/                      # Regras de Negócio
│   │   │   ├── __init__.py
│   │   │   ├── partida_competitiva_classica.py
│   │   │   └── partida_treino_classica.py
│   │   │
│   │   ├── registry/                       # Registro Dinâmico de Modos
│   │   │   ├── __init__.py
│   │   │   └── partida_registry.py         # Decorator para registrar jogos
│   │   │
│   │   └── shared/                         # Utilitários
│   │       ├── __init__.py
│   │       ├── mixins.py                   # Serialização e Permutação
│   │       └── factories.py                # Factory Method
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── repositories/                   # Arquivos/Banco
│   │   │   └── pacote_arquivo.py
│   │   └── api/                            
│   │       └── routes.py                   # Endpoints da API
│   │
│   └── main.py
│
├── data/                                   # Arquivos JSON
├── tests/                                  # Testes Automatizados (Pytest)
├── docs/                                   # Documentação
└── requirements.txt
```
