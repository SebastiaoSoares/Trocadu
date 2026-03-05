import os
import uuid
from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from src.infrastructure.repositories.pacote_arquivo import PacoteArquivo
from src.domain.shared.factories import PartidaFactory

partidas_ativas: Dict[str, Any] = {}
router = APIRouter()

@router.post("/iniciar")
def iniciar():
    """Instancia a sessão de treino solo em memória."""
    caminho_json = os.path.join(os.getcwd(), "src", "data", "palavras.json")
    banco_de_palavras = PacoteArquivo(caminho_arquivo=caminho_json)
    
    partida = PartidaFactory.criar_partida("TREINO_CLASSICA", [], banco_de_palavras)
    resultado = partida.iniciar_jogo()
    
    partida_id = str(uuid.uuid4())
    partidas_ativas[partida_id] = partida
    
    return {"partida_id": partida_id, "detalhes": resultado}

@router.post("/{partida_id}/avancar")
def avancar(partida_id: str):
    """Gera uma nova rodada indefinidamente no treino."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")
    return jogo.avancar()

@router.post("/{partida_id}/contabilizar")
def contabilizar(partida_id: str):
    """Registra o acerto e sorteia a próxima palavra do treino."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou treino não encontrado.")
    
    nova_palavra = jogo._pacote_palavras.obter_palavras()[0].termo
    jogo._turno_atual.definir_palavra(nova_palavra)
    return {"mensagem": "Acertou! Pode continuar.", "nova_palavra": nova_palavra}

@router.post("/{partida_id}/pular")
def pular(partida_id: str):
    """Sorteia uma nova palavra ignorando limites de saltos no treino."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou treino não encontrado.")
        
    nova_palavra = jogo._pacote_palavras.obter_palavras()[0].termo 
    jogo._turno_atual.definir_palavra(nova_palavra)
    return {"mensagem": "Pulou!", "nova_palavra": nova_palavra}

@router.post("/{partida_id}/encerrar")
def encerrar(partida_id: str):
    """Conclui a sessão de treino manualmente e retorna o resumo."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")
    return jogo.encerrar_manualmente()

@router.get("/{partida_id}/status")
def status(partida_id: str):
    """Retorna o estado do treino e as rodadas totais jogadas."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")
        
    return {
        "status": jogo._status.value,
        "rodadas_jogadas": getattr(jogo, '_rodadas_jogadas', 0),
        "palavra_atual": jogo._turno_atual.palavra_atual if getattr(jogo, '_turno_atual', None) else None
    }
