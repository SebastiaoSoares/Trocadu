"""Módulo contendo a entidade Turno para controlo de tempo e ações."""

from typing import Dict
from datetime import datetime, timedelta
from src.domain.entities.equipe import Equipe
from src.domain.entities.jogador import Jogador

class Turno:
    """Gere o ciclo de vida, o tempo e os papéis de uma jogada individual.

    Attributes:
        dupla (Equipe): A equipa (dupla de jogadores) ativa neste turno.
        tempo_limite (int): O tempo máximo em segundos permitido para o turno.
        palavras_disponiveis (int): A quantidade de palavras que ainda podem ser jogadas.
        palavra_atual (str): A palavra atual que deve ser adivinhada.
        timestamp_fim (datetime | None): O momento exato em que o turno deve terminar.
        guia_atual (Jogador): O jogador que está a descrever a palavra.
        adivinhador_atual (Jogador): O jogador que está a tentar adivinhar.
    """

    def __init__(self, dupla: Equipe, tempo_limite: int = 60, palavras_disponiveis: int = 4):
        """Prepara um novo turno para uma equipa específica.

        Args:
            dupla (Equipe): A equipa que jogará o turno.
            tempo_limite (int, optional): Duração do turno em segundos. Por defeito é 60.
            palavras_disponiveis (int, optional): Limite de palavras para o turno. Por defeito é 4.
        """
        self.dupla = dupla
        self.tempo_limite = tempo_limite
        self.palavras_disponiveis = palavras_disponiveis
        self.palavra_atual = ""
        self.timestamp_fim = None
        
        self.guia_atual: Jogador = dupla.jogador_1
        self.adivinhador_atual: Jogador = dupla.jogador_2

    def definir_palavra(self, palavra: str) -> None:
        """Define qual é a palavra atual a ser adivinhada.

        Args:
            palavra (str): O termo sorteado do pacote de palavras.
        """
        self.palavra_atual = palavra

    def iniciar_cronometro(self) -> None:
        """Calcula e regista a data e hora exatas em que o turno deve acabar."""
        self.timestamp_fim = datetime.utcnow() + timedelta(seconds=self.tempo_limite)

    def consumir_palavra(self) -> bool:
        """Tenta consumir uma palavra do orçamento do turno.

        Reduz o número de palavras disponíveis no turno (seja por acerto ou pulo).

        Returns:
            bool: True se ainda houver palavras disponíveis após o consumo, 
            False se o limite do turno tiver acabado.
        """
        if self.palavras_disponiveis > 0:
            self.palavras_disponiveis -= 1
            return self.palavras_disponiveis > 0
        return False

    def trocar_funcoes(self) -> Dict[str, str]:
        """Inverte os papéis entre o guia e o adivinhador.

        Returns:
            Dict[str, str]: Um dicionário contendo os nomes do novo guia e do 
            novo adivinhador para efeitos de registo/feedback.
        """
        self.guia_atual, self.adivinhador_atual = self.adivinhador_atual, self.guia_atual
        
        return {
            "novo_guia": self.guia_atual.nome,
            "novo_adivinhador": self.adivinhador_atual.nome
        }