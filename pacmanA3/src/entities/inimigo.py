"""Inimigos temáticos (vírus, spyware, ransomware, hacker)."""
import random
import pygame
from utils.config import (
    TAMANHO_CELULA, TAMANHO_SPRITE_INIMIGO, TAMANHO_HITBOX_INIMIGO,
    COLUNAS, OFFSET_Y, DURACAO_VPN,
)
from entities.direcao import Direcao
from utils.arte_coletaveis import aplicar_efeito_desconectado

_MARGEM_VISUAL = (TAMANHO_CELULA - TAMANHO_SPRITE_INIMIGO) // 2


class Inimigo:
    """Persegue o jogador ou fica vulnerável enquanto a VPN está ativa."""

    VELOCIDADE = 2

    def __init__(self, coluna: int, linha: int, cor, nome: str, icone: str,
                 sprite: pygame.Surface | None = None):
        """
        Args:
            coluna: Coluna de spawn na grade.
            linha: Linha de spawn na grade.
            cor: Cor do placeholder quando não há PNG.
            nome: Identificador do malware (ex.: Virus).
            icone: Letra exibida no placeholder procedural.
            sprite: Imagem PNG carregada ou None para desenho procedural.
        """
        self.spawn_coluna = coluna
        self.spawn_linha = linha
        self.x = float(coluna * TAMANHO_CELULA)
        self.y = float(linha * TAMANHO_CELULA)
        self.cor = cor
        self.nome = nome
        self.icone = icone
        self.sprite = sprite
        self.sprite_desconectado = (
            aplicar_efeito_desconectado(sprite) if sprite else None
        )
        self.direcao = random.choice(list(Direcao)[:-1])
        self.assustado = False
        self.timer_assustado = 0

    @property
    def rect(self) -> pygame.Rect:
        centro_x = int(self.x) + TAMANHO_CELULA // 2
        centro_y = int(self.y) + TAMANHO_CELULA // 2 + OFFSET_Y
        tamanho = TAMANHO_HITBOX_INIMIGO
        return pygame.Rect(centro_x - tamanho // 2, centro_y - tamanho // 2, tamanho, tamanho)

    def assustar(self, duracao: int = DURACAO_VPN):
        """Ativa modo vulnerável (desconectado) por alguns segundos."""
        self.assustado = True  
        self.timer_assustado = duracao

    def resetar(self):
        """Volta à posição inicial após ser neutralizado ou nova vida."""
        self.x = float(self.spawn_coluna * TAMANHO_CELULA)
        self.y = float(self.spawn_linha * TAMANHO_CELULA)
        self.assustado = False
        self.timer_assustado = 0

    def _escolher_direcao(self, mapa, coluna, linha, jogador_x, jogador_y):
        """Define próxima direção: foge aleatoriamente se assustado, senão persegue o jogador."""
        possiveis = []
        for direcao in list(Direcao)[:-1]:
            delta_col, delta_lin = direcao.value
            nova_col = (coluna + delta_col) % COLUNAS
            nova_lin = linha + delta_lin
            if 0 <= nova_lin < len(mapa) and mapa[nova_lin][nova_col] != 1:
                possiveis.append(direcao)
        if not possiveis:
            return
        if self.assustado or random.random() < 0.25:
            self.direcao = random.choice(possiveis)
            return

        def distancia(direcao):
            dc, dl = direcao.value
            alvo_x = (coluna + dc) * TAMANHO_CELULA
            alvo_y = (linha + dl) * TAMANHO_CELULA
            return (alvo_x - jogador_x) ** 2 + (alvo_y - jogador_y) ** 2

        self.direcao = min(possiveis, key=distancia)

    def atualizar(self, mapa, jogador_x: float, jogador_y: float):
        """Atualiza IA de movimento e timer do modo vulnerável."""
        if self.assustado:
            self.timer_assustado -= 1
            if self.timer_assustado <= 0:
                self.assustado = False
        coluna = int(self.x // TAMANHO_CELULA)
        linha = int(self.y // TAMANHO_CELULA)
        offset_x = self.x - coluna * TAMANHO_CELULA
        offset_y = self.y - linha * TAMANHO_CELULA
        if abs(offset_x) < self.VELOCIDADE and abs(offset_y) < self.VELOCIDADE:
            self._escolher_direcao(mapa, coluna, linha, jogador_x, jogador_y)
        delta_col, delta_lin = self.direcao.value
        novo_x = self.x + delta_col * self.VELOCIDADE
        novo_y = self.y + delta_lin * self.VELOCIDADE
        nova_coluna = int(novo_x // TAMANHO_CELULA) % COLUNAS
        nova_linha = int(novo_y // TAMANHO_CELULA)
        if 0 <= nova_linha < len(mapa) and mapa[nova_linha][nova_coluna] != 1:
            self.x = novo_x % (COLUNAS * TAMANHO_CELULA)
            self.y = novo_y

    def desenhar(self, tela: pygame.Surface):
        """Desenha sprite PNG ou placeholder; dessaturado se assustado."""
        if self.sprite is None:
            self._desenhar_placeholder(tela)
            return
        imagem = self.sprite_desconectado if self.assustado else self.sprite
        posicao = (int(self.x) + _MARGEM_VISUAL, int(self.y) + _MARGEM_VISUAL + OFFSET_Y)
        tela.blit(imagem, posicao)

    def _desenhar_placeholder(self, tela: pygame.Surface):
        """Desenha círculo colorido quando o sprite PNG do inimigo não foi carregado."""
        centro_x = int(self.x) + TAMANHO_CELULA // 2
        centro_y = int(self.y) + TAMANHO_CELULA // 2 + OFFSET_Y
        cor = (100, 100, 110) if self.assustado else self.cor
        pygame.draw.circle(tela, cor, (centro_x, centro_y), TAMANHO_CELULA // 2 - 4)
