from pydantic import BaseModel, Field

class ChutarPalavraTreinoRequest(BaseModel):
    """Schema para envio do chute da palavra no modo Treino."""
    chute: str = Field(..., min_length=1)
