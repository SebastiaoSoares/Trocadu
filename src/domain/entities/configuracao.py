class ConfiguracaoDePartida:
    """
    Encapsula as regras e limites de uma partida.
    Esta classe permite que as configurações sejam passadas de forma limpa 
    pela Factory até chegar ao Turno.
    """
    def __init__(self, tempo_limite: int = 60, palavras_por_turno: int = 4):
        self.tempo_limite = tempo_limite
        self.palavras_por_turno = palavras_por_turno
