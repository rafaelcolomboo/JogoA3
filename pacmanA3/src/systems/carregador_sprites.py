"""Carrega sprites PNG dos assets com fallback procedural."""
import os
import pygame
from utils.config import PASTA_INIMIGOS, PASTA_DADOS, IMAGENS_INIMIGOS, IMAGEM_VPN, TAMANHO_SPRITE_INIMIGO
from utils.arte_coletaveis import criar_sprite_vpn


def carregar_imagem(caminho: str, tamanho: int) -> pygame.Surface | None:
    """
    Carrega PNG e redimensiona.

    Args:
        caminho: Caminho absoluto do arquivo.
        tamanho: Largura e altura em pixels.

    Returns:
        Superfície ou None se o arquivo não existir.
    """
    if not os.path.isfile(caminho):
        return None
    imagem = pygame.image.load(caminho).convert_alpha()
    return pygame.transform.smoothscale(imagem, (tamanho, tamanho))


def carregar_sprites_inimigos() -> dict[str, pygame.Surface | None]:
    """Carrega sprites de vírus, spyware, ransomware e hacker."""
    sprites = {}
    for nome, arquivo in IMAGENS_INIMIGOS.items():
        caminho = os.path.join(PASTA_INIMIGOS, arquivo)
        sprites[nome] = carregar_imagem(caminho, TAMANHO_SPRITE_INIMIGO)
    return sprites


def carregar_sprite_vpn() -> pygame.Surface:
    """Carrega power-up VPN do disco ou gera placeholder."""
    caminho = os.path.join(PASTA_DADOS, IMAGEM_VPN)
    sprite = carregar_imagem(caminho, 20)
    return sprite if sprite else criar_sprite_vpn()
