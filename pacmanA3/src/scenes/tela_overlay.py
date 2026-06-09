"""Overlay semitransparente para morte e game over."""
import pygame
from utils.config import LARGURA, ALTURA, COR_TEXTO


def desenhar_overlay(tela, fonte_grande, fonte_media, fonte_pequena,
                     titulo: str, cor_titulo, subtitulo: str = "", linha_extra: str = ""):
    """
    Escurece a tela e exibe mensagem centralizada.

    Args:
        tela: Superfície principal.
        titulo: Texto principal (ex: GAME OVER).
        cor_titulo: Cor RGB do título.
        subtitulo: Segunda linha opcional.
        linha_extra: Terceira linha opcional (ex: ENTER para continuar).
    """
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    camada.fill((0, 0, 0, 180))
    tela.blit(camada, (0, 0))
    texto_titulo = fonte_grande.render(titulo, True, cor_titulo)
    tela.blit(texto_titulo, (LARGURA // 2 - texto_titulo.get_width() // 2, ALTURA // 2 - 80))
    if subtitulo:
        texto_sub = fonte_media.render(subtitulo, True, COR_TEXTO)
        tela.blit(texto_sub, (LARGURA // 2 - texto_sub.get_width() // 2, ALTURA // 2 - 10))
    if linha_extra:
        texto_extra = fonte_pequena.render(linha_extra, True, (160, 160, 160))
        tela.blit(texto_extra, (LARGURA // 2 - texto_extra.get_width() // 2, ALTURA // 2 + 40))
