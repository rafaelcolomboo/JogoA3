"""Sprites procedurais dos coletáveis (e-mail, localização, banco, VPN, cadeado)."""
import pygame
from utils.config import (
    COR_EMAIL, COR_LOCAL, COR_BANCO, COR_VPN, COR_CADEADO,
)


def _criar_superficie(tamanho: int) -> pygame.Surface:
    return pygame.Surface((tamanho, tamanho), pygame.SRCALPHA)


def _pintar_pixel(superficie, x, y, cor):
    if 0 <= x < superficie.get_width() and 0 <= y < superficie.get_height():
        superficie.set_at((x, y), cor)


def criar_sprite_email() -> pygame.Surface:
    """Retorna ícone de envelope 10x10 em verde neon."""
    sprite = _criar_superficie(10)
    cor, detalhe = COR_EMAIL, (0, 180, 40, 255)
    for x in range(1, 9):
        _pintar_pixel(sprite, x, 2, cor)
        _pintar_pixel(sprite, x, 7, cor)
    for y in range(3, 7):
        _pintar_pixel(sprite, 1, y, cor)
        _pintar_pixel(sprite, 8, y, cor)
    for i in range(4):
        _pintar_pixel(sprite, 2 + i, 3 + i, detalhe)
        _pintar_pixel(sprite, 7 - i, 3 + i, detalhe)
    return sprite


def criar_sprite_localizacao() -> pygame.Surface:
    """Retorna pin de mapa 14x14 em laranja."""
    sprite = _criar_superficie(14)
    cor = COR_LOCAL + (255,)
    pygame.draw.circle(sprite, cor, (7, 5), 4)
    pygame.draw.rect(sprite, cor, (5, 5, 4, 3))
    pygame.draw.polygon(sprite, cor, [(7, 12), (4, 7), (10, 7)])
    return sprite


def criar_sprite_bancario() -> pygame.Surface:
    """Retorna cartão/cifrão 16x16 em dourado."""
    sprite = _criar_superficie(16)
    cor = COR_BANCO + (255,)
    pygame.draw.rect(sprite, cor, (2, 4, 12, 9), border_radius=2)
    fonte = pygame.font.SysFont("consolas", 10, bold=True)
    sprite.blit(fonte.render("$", True, (40, 30, 0)), (5, 5))
    return sprite


def criar_sprite_vpn() -> pygame.Surface:
    """Retorna escudo com cadeado 20x20 em verde."""
    sprite = _criar_superficie(20)
    cor = COR_VPN + (255,)
    pontos = [(10, 2), (17, 6), (15, 17), (5, 17), (3, 6)]
    pygame.draw.polygon(sprite, cor, pontos)
    pygame.draw.polygon(sprite, (0, 180, 50, 255), pontos, 2)
    pygame.draw.rect(sprite, (0, 60, 20, 255), (8, 9, 4, 5))
    return sprite


def criar_sprite_cadeado() -> pygame.Surface:
    """Retorna ícone de cadeado 16x16 para vidas no HUD."""
    sprite = _criar_superficie(16)
    cor = COR_CADEADO + (255,)
    pygame.draw.rect(sprite, cor, (4, 8, 8, 7), border_radius=1)
    pygame.draw.arc(sprite, cor, (5, 2, 6, 8), 0, 3.14, 2)
    return sprite


def aplicar_efeito_desconectado(sprite: pygame.Surface) -> pygame.Surface:
    """Deixa sprite de inimigo dessaturado e semi-transparente (modo VPN)."""
    copia = sprite.copy()
    copia.fill((120, 120, 130, 255), special_flags=pygame.BLEND_RGBA_MULT)
    copia.set_alpha(130)
    return copia
