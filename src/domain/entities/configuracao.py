"""Módulo contendo a entidade de configuração da partida."""

class ConfiguracaoDePartida:
    """Encapsula as regras e limites de uma partida.

    Esta classe permite que as configurações sejam passadas de forma limpa 
    pela Factory até chegar ao Turno, centralizando os parâmetros que 
    afetam a jogabilidade e a duração do jogo.

    Attributes:
        tempo_limite (int): O tempo máximo permitido para cada turno, em segundos.
        palavras_por_turno (int): O número de palavras que uma dupla tem 
            disponível para tentar adivinhar (ou pular) num único turno.
    """
    
    def __init__(self, tempo_limite: int = 60, palavras_por_turno: int = 4):
        """Inicializa uma nova configuração de partida.

        Args:
            tempo_limite (int, optional): A duração de cada turno em segundos. 
                O valor padrão é 60.
            palavras_por_turno (int, optional): A quantidade de palavras 
                disponíveis por turno. O valor padrão é 4.
        """
        self.tempo_limite = tempo_limite
        self.palavras_por_turno = palavras_por_turno