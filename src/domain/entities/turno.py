from src.domain.entities.equipe import Equipe
from src.domain.entities.jogador import Jogador

class Turno:
    """
    Controla o ciclo micro do jogo: cronômetro, palavra ativa e validação de pulos.
    Ref: Diagrama de Classes [Turno]
    """
    def __init__(self, dupla: Equipe, tempo_limite: int = 60):
        self.dupla = dupla
        self.tempo_limite = tempo_limite
        self.palavra_atual = ""
        
        self.guia_atual: Jogador = dupla.jogador_1
        self.adivinhador_atual: Jogador = dupla.jogador_2

    def definir_palavra(self, palavra: str):
        """
        Define a palavra secreta da rodada.
        """
        self.palavra_atual = palavra

    def iniciar_cronometro(self):
        """
        Inicia a contagem do cronômetro.
        """
        print(f"=== TURNO INICIADO: {self.tempo_limite} segundos ===")
        print(f"Guia: {self.guia_atual.obter_nome()} | Adivinhador: {self.adivinhador_atual.obter_nome()}")

    def validar_chute(self, chute: str) -> bool:
        """
        Verifica se o chute corresponde à palavra atual (ignorando maiúsculas).
        """
        if not chute or not self.palavra_atual:
            return False
            
        acertou = chute.strip().lower() == self.palavra_atual.strip().lower()
        
        if acertou:
            print(f"ACERTOU! A palavra era '{self.palavra_atual}'")
        else:
            print(f"Errou: '{chute}' não é '{self.palavra_atual}'")
            
        return acertou

    def trocar_funcoes(self):
        """
        Inverte os papéis: quem era Guia vira Adivinhador e vice-versa.
        Importante para a regra de 'Ida e Volta'.
        """
        temp = self.guia_atual
        self.guia_atual = self.adivinhador_atual
        self.adivinhador_atual = temp
        
        print(f"Troca de papéis! Novo Guia: {self.guia_atual.obter_nome()}")