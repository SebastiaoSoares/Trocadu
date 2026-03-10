"""Módulo contendo a implementação do repositório de palavras personalizadas vinculadas a um utilizador."""

from uuid import UUID
from typing import List, Optional
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras
from src.domain.entities.palavra import Palavra
from src.infrastructure.database.database import SessionLocal
from src.infrastructure.database.models import PalavraModel, PacoteModel

class PacotePersonalizado(PacoteDePalavras):
    """Implementa a busca de palavras criadas por um utilizador específico na base de dados SQLite.

    Esta classe atua como uma estratégia concreta para o fornecimento de palavras, 
    consultando a base de dados relacional para carregar pacotes customizados 
    vinculados à conta de um jogador.

    Attributes:
        id_usuario (str): O identificador único (convertido para string) do utilizador dono do pacote.
        id_pacote (int | None): O identificador numérico do pacote específico a ser carregado. 
            Se for `None`, indica que todas as palavras do utilizador devem ser carregadas.
    """

    def __init__(self, id_usuario: UUID, id_pacote: Optional[int] = None):
        """Inicializa o repositório com o ID do utilizador e, opcionalmente, um ID de pacote.

        Args:
            id_usuario (UUID): O identificador único do utilizador (geralmente extraído do token de autenticação).
            id_pacote (int, optional): O ID de um pacote de palavras específico. 
                Se omitido (valor `None`), as palavras de todos os pacotes do utilizador serão carregadas.
        """
        self.id_usuario = str(id_usuario)
        self.id_pacote = id_pacote

    def obter_palavras(self) -> List[Palavra]:
        """Consulta a base de dados, filtra por utilizador/pacote e converte para objetos de domínio.

        Abre uma sessão segura com a base de dados, realiza um JOIN entre as tabelas 
        `PalavraModel` e `PacoteModel`, aplica os filtros configurados no construtor 
        e mapeia os resultados para instâncias da entidade `Palavra`. A sessão é 
        fechada automaticamente no bloco `finally`.

        Returns:
            List[Palavra]: Uma lista de objetos da entidade `Palavra` preenchidos 
            com os dados extraídos do banco de dados.

        Raises:
            ValueError: Se a consulta não retornar nenhuma palavra para os 
            critérios de pacote ou utilizador fornecidos.
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