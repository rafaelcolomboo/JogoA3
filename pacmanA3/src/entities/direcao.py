"""Enumeração das direções de movimento no grid."""
from enum import Enum


class Direcao(Enum):
    """Direções possíveis para o jogador e inimigos."""

    CIMA = (0, -1)
    BAIXO = (0, 1)
    ESQUERDA = (-1, 0)
    DIREITA = (1, 0)
    PARADO = (0, 0)
