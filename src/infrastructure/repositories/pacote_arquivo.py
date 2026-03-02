"""
Implementação de fonte de palavras baseada em arquivos JSON locais.
"""

import json
import os
from typing import List
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras
from src.domain.entities.palavra import Palavra

class PacoteArquivo(PacoteDePalavras):
    """
    Busca palavras em um arquivo JSON local.
    """

    def __init__(self, caminho_arquivo: str):
        """
        Inicializa com o caminho do arquivo.
        """
        self.caminho = caminho_arquivo

    def obter_palavras(self) -> List[Palavra]:
        """
        Lê o JSON e converte para objetos Palavra.
        """
        if not os.path.exists(self.caminho):
            raise FileNotFoundError(f"Arquivo não encontrado: {self.caminho}")

        with open(self.caminho, 'r', encoding='utf-8') as f:
            dados = json.load(f)

        return [
            Palavra(
                termo=item['termo'],
                dica=item.get('dica', ''),
                categoria=item.get('categoria', 'Geral')
            )
            for item in dados
        ]