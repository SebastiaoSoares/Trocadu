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
        <<Abstract>>
        +obter_palavras()* List~str~
    }
    
    class PacoteArquivo {
        -caminho_arquivo: str
        +obter_palavras() List~str~
    }
    
    class PacotePersonalizado {
        -lista_manual: List~str~
        +obter_palavras() List~str~
    }

    PacoteDePalavras <|-- PacoteArquivo
    PacoteDePalavras <|-- PacotePersonalizado

    class BancoDePalavras {
        -estrategia: PacoteDePalavras
        +definir_estrategia(pct: PacoteDePalavras)
        +get_palavra_aleatoria() str
    }

    BancoDePalavras o-- PacoteDePalavras : "Usa (Strategy)"

    class JsonSerializavelMixin {
        <<Mixin>>
        +to_json() dict
        +from_json(data: dict)
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
        +registrar_pontos_rodada()
    }

    JsonSerializavelMixin <|-- Usuario
    JsonSerializavelMixin <|-- Equipe

    Equipe o-- Jogador : "Agrupa Temporariamente"
    Jogador --> Usuario : "Identifica"

    class GerenciadorDePartida {
        <<Abstract>>
        #pool_jogadores: List~Jogador~
        #dupla_atual: Equipe
        #turno_atual: Turno
        #banco_palavras: BancoDePalavras
        +iniciar_jogo() final
        #gerar_permutacoes_duplas()
        #executar_rodada_ida_e_volta()
        #setup()*
        #processar_vitoria()*
    }

    class PartidaCompetitiva {
        -ranking: dict
        #setup()
        #processar_vitoria()
    }

    class PartidaTreino {
        #setup()
        #processar_vitoria()
    }

    GerenciadorDePartida <|-- PartidaCompetitiva
    GerenciadorDePartida <|-- PartidaTreino
    
    GerenciadorDePartida *-- Turno
    GerenciadorDePartida --> BancoDePalavras

    class Turno {
        -dupla: Equipe
        -guia_atual: Jogador
        -adivinhador_atual: Jogador
        -palavra: str
        -tempo_restante: int
        +iniciar_cronometro()
        +validar_chute(str) bool
        +trocar_funcoes()
    }

    Turno --> Equipe : "Contexto da Rodada"
    Turno --> Jogador : "Papéis Ativos"

    class ConfiguracaoDePartida {
        <<DTO>>
        +tempo_limite: int
        +modo_troca_duplas: bool
    }

    class NivelDificuldade {
        <<Enum>>
        FACIL
        MEDIO
        DIFICIL
    }

    class PartidaFactory {
        <<Factory>>
        +criar_partida(tipo: str, config: Config) GerenciadorDePartida
    }

    class HistoricoPartidas {
        <<Container>>
        -logs: List
    }

    ConfiguracaoDePartida --> NivelDificuldade
    PartidaFactory ..> GerenciadorDePartida : "Cria"
    HistoricoPartidas ..> JsonSerializavelMixin
```


## Definição da Estrutura de Pastas

```
Trocadu/
├── src/
│   ├── domain/                             
│   │   ├── __init__.py
│   │   │
│   │   ├── entities/                       # Entidades (SRP: Guardam estado e comportamento unitário)
│   │   │   ├── __init__.py
│   │   │   ├── jogador.py
│   │   │   ├── equipe.py
│   │   │   ├── placar.py
│   │   │   ├── turno.py
│   │   │   └── palavra.py
│   │   │
│   │   ├── interfaces/                     # Abstrações (DIP: O núcleo depende disso, não de implementações)
│   │   │   ├── __init__.py
│   │   │   ├── partida_base.py             # Define o contrato do jogo
│   │   │   └── repositorio_palavras.py     # Define o contrato de dados
│   │   │
│   │   ├── use_cases/                      # Regras Específicas (OCP: Extensões do jogo)
│   │   │   ├── __init__.py
│   │   │   ├── partida_competitiva.py
│   │   │   └── partida_treino.py
│   │   │
│   │   └── shared/                         # Utilitários e Mixins
│   │       ├── __init__.py
│   │       ├── mixins.py
│   │       └── factories.py
│   │
│   ├── infrastructure/
│   │   ├── __init__.py
│   │   ├── repositories/                   # Implementação concreta dos dados
│   │   │   └── pacote_arquivo.py
│   │   └── api/                            # FastAPI
│   │       └── routes.py
│   │
│   └── main.py
│
├── data/                                   # Arquivos JSON/SQLite
├── tests/                                  # Testes Automatizados
├── docs/                                   # Documentação
└── requirements.txt
```
