from typing import Dict
from src.domain.entities.equipe import Equipe
from src.domain.entities.jogador import Jogador

class Turno:
    """
    Controla o ciclo micro do jogo: cronômetro, palavra ativa e validação de pulos.
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
        pass

    def validar_chute(self, chute: str) -> bool:
        """
        Retorna True/False. Não imprime nada.
        """
        if not chute or not self.palavra_atual:
            return False
            
        return chute.strip().lower() == self.palavra_atual.strip().lower()

    def trocar_funcoes(self) -> Dict[str, str]:
        """
        Inverte papéis e retorna os novos papéis para log/feedback.
        """
        self.guia_atual, self.adivinhador_atual = self.adivinhador_atual, self.guia_atual
        
        return {
            "novo_guia": self.guia_atual.obter_nome(),
            "novo_adivinhador": self.adivinhador_atual.obter_nome()
        }