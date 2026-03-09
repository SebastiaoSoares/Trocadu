from pydantic import BaseModel, Field
from typing import List, Optional

class ConfiguracaoCompetitiva(BaseModel):
    """Schema de configurações do modo Clássica Competitiva."""
    palavras_por_turno: int = Field(default=4, ge=2, le=8, description="Palavras disponíveis no turno")
    tempo_limite_segundos: int = Field(default=60, ge=30, le=120, description="Tempo de cada rodada")
    id_pacote_palavras: str = Field(default="padrao", description="ID do pacote escolhido")

class CriarCompetitivaRequest(BaseModel):
    """Schema para criação de partida competitiva."""
    jogadores: List[str] = Field(..., min_length=3)
    configuracoes: Optional[ConfiguracaoCompetitiva] = Field(default_factory=ConfiguracaoCompetitiva)