"""Módulo contendo a implementação do repositório de palavras baseado em arquivos JSON locais."""

import json
import os
from typing import List
from src.domain.interfaces.repositorio_palavras import PacoteDePalavras
from src.domain.entities.palavra import Palavra

class PacoteArquivo(PacoteDePalavras):
    """Implementa a busca de palavras a partir de um ficheiro JSON local.

    Esta classe atua como uma estratégia concreta para o fornecimento de palavras, 
    carregando os dados de um ficheiro estático no sistema de ficheiros e 
    convertendo-os para as entidades do domínio.

    Attributes:
        caminho (str): O caminho absoluto ou relativo para o ficheiro JSON 
            que contém as palavras a serem carregadas.
    """

    def __init__(self, caminho_arquivo: str):
        """Inicializa o repositório de arquivo com o caminho especificado.

        Args:
            caminho_arquivo (str): O caminho completo ou relativo para o ficheiro 
                JSON contendo as palavras (ex: 'src/data/palavras.json').
        """
        self.caminho = caminho_arquivo

    def obter_palavras(self) -> List[Palavra]:
        """Lê o ficheiro JSON e converte o seu conteúdo para objetos Palavra.

        Abre o ficheiro em modo de leitura com codificação UTF-8, analisa a 
        estrutura JSON esperada e instancia os objetos da entidade `Palavra`.

        Returns:
            List[Palavra]: Uma lista contendo todas as palavras instanciadas 
            a partir dos dados do ficheiro.

        Raises:
            FileNotFoundError: Se o ficheiro especificado no atributo `caminho` 
            não existir ou não puder ser encontrado no sistema.
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