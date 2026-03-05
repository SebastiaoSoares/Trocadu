import os
import uuid
from typing import Dict, Any
from fastapi import APIRouter, HTTPException

from src.infrastructure.repositories.pacote_arquivo import PacoteArquivo
from src.domain.shared.factories import PartidaFactory
from src.domain.entities.jogador import Jogador
from src.domain.entities.configuracao import ConfiguracaoDePartida
from src.infrastructure.api.v1.schemas.partidas.classica_competitiva import (
    CriarCompetitivaRequest,
    ConfiguracaoCompetitiva
)

partidas_ativas: Dict[str, Any] = {}
router = APIRouter()

@router.get("/")
def informacoes_do_modo():
    """Retorna a estrutura, os limites e os tipos dos campos do modo usando JSON Schema."""
    return ConfiguracaoCompetitiva.model_json_schema()

@router.post("/iniciar")
def iniciar(request: CriarCompetitivaRequest):
    """Instancia a partida competitiva e a salva em memória."""
    caminho_json = os.path.join(os.getcwd(), "src", "data", "palavras.json")
    banco_de_palavras = PacoteArquivo(caminho_arquivo=caminho_json)
    
    pool_jogadores = [Jogador(nome) for nome in request.jogadores]
    
    # Conversão do Schema da API (Pydantic) para a Entidade de Domínio (POO pura)
    config_dominio = ConfiguracaoDePartida(
        tempo_limite=request.configuracoes.tempo_limite_segundos,
        limite_saltos=request.configuracoes.limite_saltos
    )
    
    partida = PartidaFactory.criar_partida(
        "COMPETITIVA_CLASSICA", 
        pool_jogadores, 
        banco_de_palavras, 
        config_dominio
    )
    resultado = partida.iniciar_jogo()
    
    partida_id = str(uuid.uuid4())
    partidas_ativas[partida_id] = partida
    
    return {
        "partida_id": partida_id, 
        "detalhes": resultado, 
        "configuracoes": request.configuracoes.model_dump()
    }

@router.post("/{partida_id}/avancar")
def avancar(partida_id: str):
    """Gera a próxima rodada ou encerra o jogo caso a fila acabe."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
    return jogo.avancar()

@router.post("/{partida_id}/contabilizar")
def contabilizar(partida_id: str):
    """Registra o acerto, computa os pontos da rodada e sorteia a próxima palavra."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou partida não encontrada.")
    
    resultado_pontos = jogo.computar_pontos_rodada(10)
    nova_palavra = jogo._pacote_palavras.obter_palavras()[0].termo
    jogo._turno_atual.definir_palavra(nova_palavra)
    
    return {"mensagem": "Ponto registrado!", "detalhes": resultado_pontos, "nova_palavra": nova_palavra}

@router.post("/{partida_id}/pular")
def pular(partida_id: str):
    """Desconta um salto da dupla e define uma nova palavra."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou partida não encontrada.")
        
    if jogo._turno_atual.pular_palavra():
        nova_palavra = jogo._pacote_palavras.obter_palavras()[0].termo 
        jogo._turno_atual.definir_palavra(nova_palavra)
        return {"mensagem": "Pulou!", "saltos_restantes": jogo._turno_atual.saltos_disponiveis, "nova_palavra": nova_palavra}
    
    raise HTTPException(status_code=400, detail="Limite de saltos excedido.")

@router.get("/{partida_id}/status")
def status(partida_id: str):
    """Retorna o estado atual da rodada e o ranking parcial."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
        
    return {
        "status": jogo._status.value,
        "ranking": getattr(jogo, '_ranking', {}),
        "turno_atual": {
            "guia": jogo._turno_atual.guia_atual.nome,
            "adivinhador": jogo._turno_atual.adivinhador_atual.nome,
            "palavra": jogo._turno_atual.palavra_atual,
            "saltos_disponiveis": getattr(jogo._turno_atual, 'saltos_disponiveis', 0)
        } if getattr(jogo, '_turno_atual', None) else None
    }
