from pydantic import BaseModel, Field
from typing import List, Optional


class PalavraBase(BaseModel):
    termo: str = Field(..., description="A palavra a ser adivinhada")
    dica: Optional[str] = Field(default="", description="Dica opcional para a palavra")
    categoria: Optional[str] = Field(default="Personalizado", description="Categoria da palavra")

class PalavraResponse(PalavraBase):
    id: int

    class Config:
        from_attributes = True


class PacoteCreate(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome do pacote")
    descricao: Optional[str] = Field(default=None, description="Descrição do pacote")
    palavras: List[PalavraBase] = Field(..., min_items=1, description="Lista de palavras do pacote")

class PacoteUpdate(BaseModel):
    nome: Optional[str] = Field(default=None, min_length=1)
    descricao: Optional[str] = Field(default=None)
    palavras: Optional[List[PalavraBase]] = Field(default=None, min_items=1)

class PacoteResponse(BaseModel):
    id: int
    usuario_id: str
    nome: str
    descricao: Optional[str]
    palavras: List[PalavraResponse]

    class Config:
        from_attributes = True
