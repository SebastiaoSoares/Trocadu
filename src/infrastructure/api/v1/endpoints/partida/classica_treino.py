import os
import uuid
import random
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status

from src.infrastructure.repositories.pacote_arquivo import PacoteArquivo
from src.domain.shared.factories import PartidaFactory

partidas_ativas: Dict[str, Any] = {}
router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_treino():
    """Instancia a sessão de treino solo em memória (criação do recurso)."""
    caminho_json = os.path.join(os.getcwd(), "src", "data", "palavras.json")
    banco_de_palavras = PacoteArquivo(caminho_arquivo=caminho_json)
    
    partida = PartidaFactory.criar_partida("TREINO_CLASSICA", [], banco_de_palavras)
    resultado = partida.iniciar_jogo()
    
    partida_id = str(uuid.uuid4())
    partidas_ativas[partida_id] = partida
    
    return {"partida_id": partida_id, "detalhes": resultado}

@router.get("/{partida_id}", status_code=status.HTTP_200_OK)
def obter_treino(partida_id: str):
    """Retorna o estado do recurso treino e as rodadas totais jogadas."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")
        
    return {
        "status": jogo._status.value,
        "rodadas_jogadas": getattr(jogo, '_rodadas_jogadas', 0),
        "palavra_atual": jogo._turno_atual.palavra_atual if getattr(jogo, '_turno_atual', None) else None
    }

@router.post("/{partida_id}/turnos", status_code=status.HTTP_201_CREATED)
def criar_turno(partida_id: str):
    """Gera uma nova rodada (novo turno) indefinidamente no treino."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")
    
    resultado = jogo.avancar()
    
    if resultado.get("status") == "RODADA_NOVA" and jogo._turno_atual.timestamp_fim:
        resultado["timestamp_fim"] = jogo._turno_atual.timestamp_fim.isoformat() + "Z"
        
    return resultado

@router.post("/{partida_id}/pontuacoes", status_code=status.HTTP_201_CREATED)
def adicionar_pontuacao(partida_id: str):
    """Registra o acerto (cria pontuação) e sorteia a próxima palavra do treino."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou treino não encontrado.")
    
    palavras_disponiveis = jogo._pacote_palavras.obter_palavras()
    nova_palavra = random.choice(palavras_disponiveis).termo
    
    jogo._turno_atual.definir_palavra(nova_palavra)
    return {"mensagem": "Acertou! Pode continuar.", "nova_palavra": nova_palavra}

@router.post("/{partida_id}/saltos", status_code=status.HTTP_201_CREATED)
def registrar_salto(partida_id: str):
    """Salta e sorteia uma nova palavra."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou treino não encontrado.")
        
    palavras_disponiveis = jogo._pacote_palavras.obter_palavras()
    nova_palavra = random.choice(palavras_disponiveis).termo 
    
    jogo._turno_atual.definir_palavra(nova_palavra)
    return {"mensagem": "Pulou!", "nova_palavra": nova_palavra}

@router.patch("/{partida_id}", status_code=status.HTTP_200_OK)
def encerrar_treino(partida_id: str):
    """Conclui a sessão de treino manualmente (atualização de estado) e retorna o resumo."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Treino não encontrado.")
    return jogo.encerrar_manualmente()