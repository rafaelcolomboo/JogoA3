"""Coletáveis do mapa: e-mail, localização, dados bancários e VPN."""
import pygame
from enum import Enum
from utils.config import (
TAMANHO_CELULA, OFFSET_Y, VALOR_EMAIL, VALOR_LOCAL, VALOR_BANCO,
    COR_EMAIL, COR_LOCAL, COR_BANCO, COR_VPN,
)
from utils import arte_coletaveis


class TipoDado(Enum):
    """Tipos de dados que o jogador pode coletar."""

    EMAIL = "email"
    LOCALIZACAO = "localizacao"
    BANCARIO = "bancario"
    VPN = "vpn"


_DADOS_INFO = {
    TipoDado.EMAIL: (VALOR_EMAIL, "+10 e-mail", COR_EMAIL),
    TipoDado.LOCALIZACAO: (VALOR_LOCAL, "+30 localizacao", COR_LOCAL),
    TipoDado.BANCARIO: (VALOR_BANCO, "+50 dados bancarios", COR_BANCO),
    TipoDado.VPN: (0, "VPN ativada!", COR_VPN),
}

_FALLBACKS = {
    TipoDado.EMAIL: arte_coletaveis.criar_sprite_email,
    TipoDado.LOCALIZACAO: arte_coletaveis.criar_sprite_localizacao,
    TipoDado.BANCARIO: arte_coletaveis.criar_sprite_bancario,
    TipoDado.VPN: arte_coletaveis.criar_sprite_vpn,
}


class Dado:
    """Representa um item coletável posicionado no mapa."""

    def __init__(self, coluna: int, linha: int, tipo: TipoDado,
                 sprite: pygame.Surface | None = None):
        """
        Args:
            coluna: Coluna na grade do mapa.
            linha: Linha na grade do mapa.
            tipo: Categoria do dado coletável.
            sprite: Superfície opcional; usa arte procedural se None.
        """
        self.coluna = coluna
        self.linha = linha
        self.tipo = tipo
        self.coletado = False
        self.sprite = sprite
        valor, texto_feedback, cor = _DADOS_INFO[tipo]
        self.valor = valor
        self.feedback = texto_feedback
        self.cor_feedback = cor
        self.mega = tipo == TipoDado.VPN

    def desenhar(self, tela: pygame.Surface):
        """Desenha o coletável no centro da célula, se ainda não foi coletado."""
        if self.coletado:
            return
        centro_x = self.coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
        centro_y = self.linha * TAMANHO_CELULA + TAMANHO_CELULA // 2 + OFFSET_Y
        sprite = self.sprite or _FALLBACKS[self.tipo]()
        tela.blit(sprite, sprite.get_rect(center=(centro_x, centro_y)))
