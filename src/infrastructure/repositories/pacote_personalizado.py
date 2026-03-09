"""
Implementação de fonte de palavras personalizadas vinculadas a um usuário.
"""

from uuid import UUID
from typing import List
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras
from src.domain.entities.palavra import Palavra
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.models import PalavraModel, PacoteModel

class PacotePersonalizado(PacoteDePalavras):
    """
    Busca palavras criadas por um usuário específico no banco de dados SQLite.
    """

    def __init__(self, id_usuario: UUID, id_pacote: int = None):
        """
        Inicializa com o ID do usuário e, opcionalmente, o ID de um pacote específico.
        Se o id_pacote não for fornecido, pode carregar todas as palavras do usuário.
        """
        self.id_usuario = str(id_usuario)
        self.id_pacote = id_pacote

    def obter_palavras(self) -> List[Palavra]:
        """
        Abre a sessão com o banco, faz o JOIN entre Palavra e Pacote e retorna as Entidades.
        """
        db = SessionLocal()
        try:
            query = db.query(PalavraModel).join(PacoteModel).filter(
                PacoteModel.usuario_id == self.id_usuario
            )
            
            if self.id_pacote:
                query = query.filter(PacoteModel.id == self.id_pacote)
                
            palavras_db = query.all()
            
            if not palavras_db:
                raise ValueError("Nenhuma palavra encontrada para este pacote/usuário.")

            return [
                Palavra(
                    termo=p.termo,
                    dica=p.dica or "",
                    categoria=p.categoria or "Personalizado"
                )
                for p in palavras_db
            ]
        finally:
            db.close()