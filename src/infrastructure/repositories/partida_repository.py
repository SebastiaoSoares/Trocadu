from sqlalchemy.orm import Session
from src.infrastructure.database.models import PartidaModel, ResultadoModel

class PartidaRepository:
    def __init__(self, session: Session):
        self.session = session

    def salvar_historico(self, tipo_partida: str, ranking: list):
        nova_partida = PartidaModel(tipo=tipo_partida)
        self.session.add(nova_partida)
        self.session.flush()

        for item in ranking:
            resultado = ResultadoModel(
                partida_id=nova_partida.id,
                nome_jogador=item['nome'],
                pontos=item['pontos'],
                posicao=item['posicao']
            )
            self.session.add(resultado)
        
        self.session.commit()