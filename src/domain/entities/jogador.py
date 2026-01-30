from src.dominio.usuario import Usuario

class Jogador:
    """
    Representa quem joga a sessão atual; vincula um Usuário a uma Equipe.
    """
    
    def __init__(self, usuario: Usuario):
        self.usuario_ref = usuario
        self.pontuacao_individual = 0

    def incrementar_pontos(self, qtd: int):
        self.pontuacao_individual += qtd

    def obter_nome(self) -> str:
        return self.usuario_ref.nickname