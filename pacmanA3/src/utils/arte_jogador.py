"""Sprites e animação procedural do avatar do jogador."""
import pygame
from src.entities.direcao import Direcao
from src.utils.config import COR_AVATAR, TAMANHO_AVATAR


def _criar_superficie() -> pygame.Surface:
    return pygame.Surface((TAMANHO_AVATAR, TAMANHO_AVATAR), pygame.SRCALPHA)


def _pintar_pixel(superficie, x, y, cor):
    if 0 <= x < TAMANHO_AVATAR and 0 <= y < TAMANHO_AVATAR:
        superficie.set_at((x, y), cor)


def _desenhar_quadro_avatar(superficie, quadro: int, deslocamento_olhar: int = 0):
    """Desenha um frame do avatar com capuz e tela no rosto."""
    azul = COR_AVATAR + (255,)
    escuro = (0, 90, 130, 255)
    tela = (20, 40, 60, 255)
    brilho = (0, 255, 220, 255)
    oscilacao = quadro % 3 - 1

    pygame.draw.ellipse(superficie, escuro, (6, 4 + oscilacao, 20, 18))
    pygame.draw.ellipse(superficie, azul, (8, 6 + oscilacao, 16, 14))
    pygame.draw.rect(superficie, tela, (10, 10 + oscilacao, 12, 9), border_radius=2)
    _pintar_pixel(superficie, 13 + deslocamento_olhar, 14 + oscilacao, brilho)
    _pintar_pixel(superficie, 16 + deslocamento_olhar, 14 + oscilacao, brilho)
    pygame.draw.polygon(superficie, escuro, [(4, 22 + oscilacao), (28, 22 + oscilacao), (26, 30), (6, 30)])
    pygame.draw.polygon(superficie, azul, [(8, 22 + oscilacao), (24, 22 + oscilacao), (22, 28), (10, 28)])


def criar_animacao_jogador() -> dict:
    """
    Gera dicionário {Direcao: [frames]} com 3 frames por direção.

    Returns:
        Mapa de superfícies animadas por direção de movimento.
    """
    deslocamento_olhar = {
        Direcao.DIREITA: 1, Direcao.ESQUERDA: -1,
        Direcao.CIMA: 0, Direcao.BAIXO: 0, Direcao.PARADO: 0,
    }
    animacao = {}
    for direcao in (Direcao.CIMA, Direcao.BAIXO, Direcao.ESQUERDA, Direcao.DIREITA, Direcao.PARADO):
        frames = []
        for quadro in range(3):
            sprite = _criar_superficie()
            _desenhar_quadro_avatar(sprite, quadro, deslocamento_olhar.get(direcao, 0))
            if direcao == Direcao.ESQUERDA:
                sprite = pygame.transform.flip(sprite, True, False)
            frames.append(sprite)
        animacao[direcao] = frames
    return animacao
