# Trocadu

Trocadu é um Party Game desenvolvido como uma API RESTful, baseando-se no paradígma da Programação Orientada a Objetos (POO).


## Instalação

Faça clone do projeto:
```bash
git clone https://github.com/SebastiaoSoares/Trocadu.git
```

Crie e entre em um ambiente virtual:
```bash
python -m venv venv

source ./venv/bin/activate # linux
.\venv\Scripts\Activate.ps1 # windows
```

Instale as dependências e execute o programa principal:
```bash
pip install -r requirements.txt
python run.py
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
        -id_usuario: str
        -id_pacote: int
        +obter_palavras() List~Palavra~
    }
    
    PacoteDePalavras <|-- PacoteArquivo
    PacoteDePalavras <|-- PacotePersonalizado

    class JsonSerializavelMixin {
        <<Mixin>>
        +to_json() str
        +to_dict() dict
        +from_json(str)$ Any
    }

    class PermutadorMixin {
        <<Mixin>>
        #gerar_permutacoes_duplas() Deque~Equipe~
        #executar_rodada_ida_e_volta(dupla: Equipe)
    }

    class Usuario {
        -id: UUID
        -nickname: str
        +atualizar_perfil(novo_nickname: str)
    }

    class Jogador {
        -nome: str
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
        +categoria: str
        +termo() str
        +dica() str
    }

    JsonSerializavelMixin <|-- Usuario
    JsonSerializavelMixin <|-- Equipe
    JsonSerializavelMixin <|-- Palavra

    Equipe o-- Jogador : "Agrupa"
    Jogador --> Usuario : "Refere-se"

    class ConfiguracaoDePartida {
        +tempo_limite: int
        +palavras_por_turno: int
    }

    class GerenciadorDePartida {
        <<Abstract>>
        #pool_jogadores: List~Jogador~
        #turno_atual: Turno
        #pacote_palavras: PacoteDePalavras
        #configuracao: ConfiguracaoDePartida
        #status: Status
        +iniciar_jogo() final
        #setup()*
        #avancar()*
        #processar_vitoria()*
    }

    class PartidaCompetitivaClassica {
        -ranking: dict
        -fila_de_duplas: deque
        -dupla_atual: Equipe
        -fase_rodada: str
        #setup()
        +avancar()
        +computar_pontos_rodada(pontos: int)
        #processar_vitoria()
    }

    class PartidaTreinoClassica {
        -jogador_usuario: Jogador
        -jogador_sistema: Jogador
        -equipe_treino: Equipe
        -rodadas_jogadas: int
        #setup()
        +avancar()
        +encerrar_manualmente()
        #processar_vitoria()
    }
    
    class PartidaRegistry {
        <<Singleton>>
        +registrar(chave: str)
        +obter_classe(chave: str) Type
        +listar_modos() list
    }

    GerenciadorDePartida *-- ConfiguracaoDePartida : "Possui"
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
        -palavras_disponiveis: int
        -timestamp_fim: datetime
        -guia_atual: Jogador
        -adivinhador_atual: Jogador
        +definir_palavra(str)
        +iniciar_cronometro()
        +consumir_palavra() bool
        +trocar_funcoes() dict
    }

    Turno --> Equipe
    
    class PartidaFactory {
        <<Factory>>
        +criar_partida(tipo: str, pool: List~Jogador~, banco: object, config: ConfiguracaoDePartida) GerenciadorDePartida
    }

    PartidaFactory ..> PartidaRegistry : "Consulta"
    PartidaFactory ..> GerenciadorDePartida : "Cria"
```


## Definição da Estrutura de Pastas

```
Trocadu/
├── docs/                               # Documentação e artefatos de planeamento
│   ├── prototype/                      # Imagens com as telas do jogo desenhadas (Wireframes)
│   │   ├── Configurações.png
│   │   ├── Home.png
│   │   ├── Inicio.png
│   │   └── Seleção-Jogo.png
│   ├── proposta_final.pdf              # Especificação e modelagem entregue
│   └── proposta_inicial.pdf
│
├── src/                                # Código-fonte principal da aplicação
│   ├── data/                           # Arquivos estáticos de dados
│   │   └── palavras.json               # Pacote padrão de palavras
│   │
│   ├── domain/                         # CAMADA DE REGRAS DE NEGÓCIO (Core/POO)
│   │   ├── entities/                   # Entidades independentes (Objetos do jogo)
│   │   │   ├── configuracao.py
│   │   │   ├── equipe.py
│   │   │   ├── jogador.py
│   │   │   ├── palavra.py
│   │   │   ├── placar.py
│   │   │   ├── turno.py
│   │   │   └── usuario.py
│   │   ├── interfaces/                 # Abstrações e Contratos (Princípio DIP do SOLID)
│   │   │   ├── partida_base.py         # Classe abstrata e Template Method
│   │   │   └── repositorio_palavras.py # Interface/Strategy para buscar palavras
│   │   ├── registry/                   # Padrão Registry
│   │   │   └── partida_registry.py     # Decorator para injetar modos de jogo
│   │   ├── shared/                     # Utilitários partilhados do domínio
│   │   │   ├── factories.py            # Padrão Factory Method
│   │   │   └── mixins.py               # Lógica de Permutação e Herança Múltipla
│   │   └── use_cases/                  # Casos de Uso (Modos de Jogo Concretos)
│   │       ├── __init__.py
│   │       ├── partida_competitiva_classica.py
│   │       └── partida_treino_classica.py
│   │
│   ├── infrastructure/                 # CAMADA DE DETALHES (DB, API, Frameworks)
│   │   ├── api/                        # Entrega Web (FastAPI)
│   │   │   ├── app.py                  # Instância principal e documentação Swagger
│   │   │   └── v1/
│   │   │       ├── endpoints/          # Controladores das rotas (Controllers)
│   │   │       │   ├── game/           # Rotas gerenciais do sistema
│   │   │       │   │   ├── auth.py
│   │   │       │   │   ├── general.py
│   │   │       │   │   ├── historico.py
│   │   │       │   │   ├── jogador.py
│   │   │       │   │   └── pacote.py
│   │   │       │   ├── partida/        # Ações específicas interagindo com Casos de Uso
│   │   │       │   │   ├── classica_competitiva.py
│   │   │       │   │   └── classica_treino.py
│   │   │       │   ├── game_routes.py
│   │   │       │   └── partida_routes.py
│   │   │       ├── routes.py           # Agregador mestre de rotas da versão 1
│   │   │       └── schemas/            # Pydantic Models (Validação de Input/Output)
│   │   │           ├── historico.py
│   │   │           ├── jogador_salvo.py
│   │   │           ├── pacote.py
│   │   │           └── partidas/
│   │   │               ├── classica_competitiva.py
│   │   │               └── classica_treino.py
│   │   ├── database/                   # Persistência com SQLAlchemy
│   │   │   ├── database.py             # Configuração do SQLite
│   │   │   └── models.py               # Mapeamento Relacional (ORM)
│   │   ├── repositories/               # Implementações dos Contratos (Repository Pattern)
│   │   │   ├── pacote_arquivo.py       # Lê do palavras.json
│   │   │   ├── pacote_personalizado.py # Lê do banco de dados (SQLite)
│   │   │   └── partida_repository.py   # Salva histórico
│   │   └── security/                   # Camada de Proteção
│   │       └── auth.py                 # Lógica de JWT e Hashing de senhas
│   │
├── tests/                              # Suite de testes automatizados (Pytest)
│   ├── test_entities.py
│   ├── test_factories.py
│   ├── test_mixins.py
│   ├── test_registry.py
│   └── test_use_cases.py               # Testes com Mocks (Cumpre requisito POO)
│
├── .env.example                        # Exemplo de variáveis de ambiente
├── .gitignore                          # Exclusões do Git
├── README.md                           # Documentação e instruções de execução
├── requirements.txt                    # Dependências do Python (FastAPI, SQLAlchemy, etc)
└── run.py                              # Ponto de entrada para iniciar o servidor Uvicorn
```
