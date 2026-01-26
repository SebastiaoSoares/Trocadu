# Trocadu

Trocadu é um Party Game desenvolvido como uma API RESTful, baseando-se no paradígma da Programação Orientada a Objetos (POO).

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
