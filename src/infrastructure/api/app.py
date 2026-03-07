import os
from dotenv import load_dotenv
from fastapi import FastAPI
from src.infrastructure.api.v1.routes import router
from src.infrastructure.database.database import criar_tabelas

description = """
API do Trocadu, jogo de palavras do gênero Party Game. Esta API é responsável por gerenciar partidas,
jogadores e pontuações, permitindo que os usuários criem e participem de partidas, além de acompanhar
seu desempenho e histórico de jogos.

O projeto, Open Source, está disponível no [GitHub](https://github.com/SebastiaoSoares/Trocadu).

Veja também o perfil dos desenvolvedores: [Sebastião Soares](https://github.com/SebastiaoSoares) | [Ramom Mascena](https://github.com/RamomRicarto) | [Sabrina Alencar](https://github.com/sabrinaalencaar)
"""

def create_app() -> FastAPI:

    load_dotenv()
    
    criar_tabelas()

    env = os.getenv("ENVIRONMENT", "production").lower()
    
    show_docs = "/docs" if env == "development" else None
    show_redoc = "/redoc" if env == "development" else None

    app = FastAPI(
        title="Trocadu API",
        version="1.0.0",
        description=description,

        docs_url=show_docs,
        redoc_url=show_redoc,
    )
    
    app.include_router(router)
    
    return app

app = create_app()
