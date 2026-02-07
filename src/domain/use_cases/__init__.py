"""
Módulo que agrega todos os casos de uso (modos de jogo) disponíveis no sistema.
"""

# Todos os modos de jogo implementados devem estar aqui,
# para que os decorators de importação dinâmica consigam
# encontrá-los automaticamente.

from .partida_competitiva_classica import PartidaCompetitivaClassica
from .partida_treino_classica import PartidaTreinoClassica