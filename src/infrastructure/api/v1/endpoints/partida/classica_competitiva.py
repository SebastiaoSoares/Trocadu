import os
import uuid
import random
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session

from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.models import PartidaModel, ResultadoModel
from src.infrastructure.security.auth import get_current_user_id_optional

from src.infrastructure.repositories.pacote_arquivo import PacoteArquivo
from src.infrastructure.repositories.pacote_personalizado import PacotePersonalizado
from src.domain.shared.factories import PartidaFactory
from src.domain.entities.jogador import Jogador
from src.domain.entities.configuracao import ConfiguracaoDePartida
from src.infrastructure.api.v1.schemas.partidas.classica_competitiva import (
    CriarCompetitivaRequest,
    ConfiguracaoCompetitiva
)

partidas_ativas: Dict[str, Any] = {}
router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/schema", status_code=status.HTTP_200_OK)
def informacoes_do_modo():
    """Retorna a estrutura, os limites e os tipos dos campos do modo usando JSON Schema."""
    return ConfiguracaoCompetitiva.model_json_schema()

@router.post("/", status_code=status.HTTP_201_CREATED)
def criar_partida(
    request: CriarCompetitivaRequest, 
    usuario_id: Optional[str] = Depends(get_current_user_id_optional)
):
    """Instancia a partida competitiva (recurso) e a salva em memória."""
    
    id_pacote_escolhido = request.configuracoes.id_pacote_palavras
    
    if id_pacote_escolhido == "padrao":
        caminho_json = os.path.join(os.getcwd(), "src", "data", "palavras.json")
        banco_de_palavras = PacoteArquivo(caminho_arquivo=caminho_json)
    else:
        if not usuario_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="É necessário iniciar sessão para utilizar pacotes personalizados."
            )
        try:
            banco_de_palavras = PacotePersonalizado(
                id_usuario=usuario_id, 
                id_pacote=int(id_pacote_escolhido)
            )
        except ValueError:
            raise HTTPException(
                status_code=400, 
                detail="O ID do pacote personalizado deve ser um número inteiro válido."
            )
    
    pool_jogadores = [Jogador(nome) for nome in request.jogadores]
    
    config_dominio = ConfiguracaoDePartida(
        palavras_por_turno=request.configuracoes.palavras_por_turno,
        tempo_limite=request.configuracoes.tempo_limite_segundos
    )
    
    try:
        partida = PartidaFactory.criar_partida(
            "COMPETITIVA_CLASSICA", 
            pool_jogadores, 
            banco_de_palavras, 
            config_dominio
        )
        resultado = partida.iniciar_jogo()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    partida_id = str(uuid.uuid4())
    
    partida.usuario_id_logado = usuario_id 
    
    partidas_ativas[partida_id] = partida
    
    return {
        "partida_id": partida_id, 
        "detalhes": resultado, 
        "configuracoes": request.configuracoes.model_dump()
    }

@router.get("/{partida_id}", status_code=status.HTTP_200_OK)
def obter_partida(partida_id: str):
    """Retorna o estado atual do recurso partida (rodada e o ranking parcial)."""
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
            "palavras_disponiveis": getattr(jogo._turno_atual, 'palavras_disponiveis', 0)
        } if getattr(jogo, '_turno_atual', None) else None
    }

@router.post("/{partida_id}/turnos", status_code=status.HTTP_201_CREATED)
def criar_turno(partida_id: str, db: Session = Depends(get_db)):
    """Cria um novo turno (gera a próxima rodada) ou encerra o jogo caso a fila acabe."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo:
        raise HTTPException(status_code=404, detail="Partida não encontrada.")
        
    resultado = jogo.avancar()
    
    if resultado.get("status") == "RODADA_NOVA" and jogo._turno_atual.timestamp_fim:
        resultado["timestamp_fim"] = jogo._turno_atual.timestamp_fim.isoformat() + "Z"
        
    elif resultado.get("status") == "FINALIZADA":
        usuario_id = getattr(jogo, "usuario_id_logado", None)
        
        if usuario_id:
            nova_partida = PartidaModel(usuario_id=usuario_id, modo_jogo="COMPETITIVA_CLASSICA")
            db.add(nova_partida)
            db.flush()
            
            ranking_ordenado = sorted(jogo._ranking.items(), key=lambda x: x[1], reverse=True)
            for index, (nome_equipe, pontos) in enumerate(ranking_ordenado):
                resultado_db = ResultadoModel(
                    partida_id=nova_partida.id,
                    equipe=nome_equipe,
                    pontuacao=pontos,
                    posicao=index + 1
                )
                db.add(resultado_db)
            
            db.commit()
            del partidas_ativas[partida_id]
            
    return resultado

@router.post("/{partida_id}/pontuacoes", status_code=status.HTTP_201_CREATED)
def adicionar_pontuacao(partida_id: str):
    """Registra o ponto e tenta sortear uma nova palavra do orçamento do turno."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou partida não encontrada.")
    
    resultado_pontos = jogo.computar_pontos_rodada(1) if jogo._turno_atual.palavras_disponiveis > 0 else jogo.computar_pontos_rodada(0)

    if jogo._turno_atual.consumir_palavra():
        palavras_db = jogo._pacote_palavras.obter_palavras()
        nova_palavra = random.choice(palavras_db).termo
        jogo._turno_atual.definir_palavra(nova_palavra)
        
        return {
            "mensagem": "Ponto registrado!", 
            "detalhes": resultado_pontos, 
            "nova_palavra": nova_palavra,
            "turno_finalizado": False
        }

    return {
        "mensagem": "Ponto registrado! O limite de palavras do turno chegou ao fim.", 
        "detalhes": resultado_pontos,
        "turno_finalizado": True
    }

@router.post("/{partida_id}/saltos", status_code=status.HTTP_201_CREATED)
def registrar_salto(partida_id: str):
    """Salta e define uma nova palavra."""
    jogo = partidas_ativas.get(partida_id)
    if not jogo or not getattr(jogo, "_turno_atual", None):
        raise HTTPException(status_code=400, detail="Turno inativo ou partida não encontrada.")
        
    if jogo._turno_atual.consumir_palavra():
        palavras_disponiveis = jogo._pacote_palavras.obter_palavras()
        nova_palavra = random.choice(palavras_disponiveis).termo 
        
        jogo._turno_atual.definir_palavra(nova_palavra)
        return {"mensagem": "Pulou!", "nova_palavra": nova_palavra}
    
    raise HTTPException(status_code=400, detail="As palavras do turno acabaram.")
