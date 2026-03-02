from typing import Dict
from src.domain.entities.equipe import Equipe
from src.domain.entities.jogador import Jogador

class Turno:
    """
    Controla o ciclo micro do jogo: cronômetro, palavra ativa e validação de pulos.
    """
    def __init__(self, dupla: Equipe, tempo_limite: int = 60, saltos_disponiveis: int = 3):
        self.dupla = dupla
        self.tempo_limite = tempo_limite
        self.saltos_disponiveis = saltos_disponiveis
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

    def pular_palavra(self) -> bool:
        """
        Tenta pular a palavra atual. Retorna True se conseguiu, False se limite excedido.
        """
        if self.saltos_disponiveis > 0:
            self.saltos_disponiveis -= 1
            return True
        return False

    def trocar_funcoes(self) -> Dict[str, str]:
        """
        Inverte papéis e retorna os novos papéis para log/feedback.
        """
        self.guia_atual, self.adivinhador_atual = self.adivinhador_atual, self.guia_atual
        
        return {
            "novo_guia": self.guia_atual.nome,
            "novo_adivinhador": self.adivinhador_atual.nome
        }