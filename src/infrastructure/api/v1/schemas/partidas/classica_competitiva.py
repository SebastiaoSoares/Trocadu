from pydantic import BaseModel, Field
from typing import List, Optional

class ConfiguracaoCompetitiva(BaseModel):
    """Schema de configurações do modo Clássica Competitiva."""
    tempo_limite_segundos: int = Field(default=60, ge=30, le=120, description="Tempo de cada rodada")
    limite_saltos: int = Field(default=3, ge=0, le=10, description="Quantas vezes a dupla pode pular")
    id_pacote_palavras: str = Field(default="padrao", description="ID do pacote escolhido")

class CriarCompetitivaRequest(BaseModel):
    """Schema para criação de partida competitiva."""
    jogadores: List[str] = Field(..., min_length=3)
    configuracoes: Optional[ConfiguracaoCompetitiva] = Field(default_factory=ConfiguracaoCompetitiva)