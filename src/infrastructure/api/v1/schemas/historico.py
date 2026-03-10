from pydantic import BaseModel
from typing import List
from datetime import datetime

class ResultadoResponse(BaseModel):
    posicao: int
    equipe: str
    pontuacao: int

    class Config:
        from_attributes = True

class PartidaHistoricoResponse(BaseModel):
    id: str
    modo_jogo: str
    data_jogada: datetime
    resultados: List[ResultadoResponse]

    class Config:
        from_attributes = True
