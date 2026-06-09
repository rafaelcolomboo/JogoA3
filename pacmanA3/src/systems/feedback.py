"""Textos flutuantes exibidos ao coletar dados."""

import pygame
from src.utils.config import DURACAO_FEEDBACK

class TextoFlutuante:

    """Mensagem temporária que sobe na tela após uma coleta."""

    def __init__(self, posicao_x: int, posicao_y: int, texto: str, cor: tuple):
        """
        Args:
            posicao_x: Centro horizontal do texto na tela.

            posicao_y: Posição vertical inicial.

            texto: Mensagem exibida (ex.: +10 e-mail).

            cor: Tupla RGBA da cor do texto.
        """
        self.posicao_x = posicao_x
        self.posicao_y = float(posicao_y)
        self.texto = texto
        self.cor = cor
        self.timer = DURACAO_FEEDBACK
        self.fonte = pygame.font.SysFont("consolas", 13, bold=True)

    def atualizar(self) -> bool:

        self.timer -= 1
        self.posicao_y -= 0.6
        return self.timer > 0

    def desenhar(self, tela: pygame.Surface):
        superficie_texto = self.fonte.render(self.texto, True, self.cor[:3])
        tela.blit(superficie_texto,
                  (self.posicao_x - superficie_texto.get_width() // 2, int(self.posicao_y)))
