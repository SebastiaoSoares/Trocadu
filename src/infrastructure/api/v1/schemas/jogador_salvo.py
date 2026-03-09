from pydantic import BaseModel, Field

class JogadorSalvoBase(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome do jogador a ser salvo")

class JogadorSalvoCreate(JogadorSalvoBase):
    pass

class JogadorSalvoUpdate(BaseModel):
    nome: str = Field(..., min_length=1)

class JogadorSalvoResponse(JogadorSalvoBase):
    id: int
    usuario_id: str

    class Config:
        from_attributes = True
