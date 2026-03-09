from typing import Dict
from datetime import datetime, timedelta
from src.domain.entities.equipe import Equipe
from src.domain.entities.jogador import Jogador

class Turno:
    def __init__(self, dupla: Equipe, tempo_limite: int = 60, palavras_disponiveis: int = 4):
        self.dupla = dupla
        self.tempo_limite = tempo_limite
        self.palavras_disponiveis = palavras_disponiveis
        self.palavra_atual = ""
        self.timestamp_fim = None
        
        self.guia_atual: Jogador = dupla.jogador_1
        self.adivinhador_atual: Jogador = dupla.jogador_2

    def definir_palavra(self, palavra: str):
        self.palavra_atual = palavra

    def iniciar_cronometro(self):
        """Calcula a data e hora exata em que o turno deve acabar."""
        self.timestamp_fim = datetime.utcnow() + timedelta(seconds=self.tempo_limite)

    def consumir_palavra(self) -> bool:
        """
        Tenta consumir uma palavra do orçamento do turno (seja por acerto ou pulo).
        Retorna True se ainda houver estoque, False se o limite do turno acabou.
        """
        if self.palavras_disponiveis > 0:
            self.palavras_disponiveis -= 1
            return self.palavras_disponiveis > 0
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
