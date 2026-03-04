import os
from fastapi import APIRouter
from src.domain.shared.factories import PartidaFactory
from src.infrastructure.repositories.pacote_arquivo import PacoteArquivo

router = APIRouter()

@router.get("/")
def health_check():
    return {"status": f"Trocadu API online! Ambiente: {os.getenv('ENV')}"}

@router.post("/partida")
def criar_partida(tipo: str):
    caminho_json = os.path.join(os.getcwd(), "src", "data", "palavras.json")
    
    banco_de_palavras = PacoteArquivo(caminho_arquivo=caminho_json)
    
    partida = PartidaFactory.criar_partida(tipo, [], banco_de_palavras)
    
    return {"mensagem": "Partida criada usando palavras.json", "tipo": tipo}