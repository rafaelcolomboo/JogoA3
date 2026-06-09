"""Renderização visual do labirinto estilo circuito de rede."""
import pygame
from utils.config import (
    COR_FUNDO, COR_GRADE, COR_PAREDE, COR_PAREDE_BORDA, COR_NO,
    TAMANHO_CELULA, COLUNAS, LINHAS, OFFSET_Y,
)

# Cache da superfície de fundo. Atenção: esta variável de módulo torna-se inválida
# se o pygame for reinicializado em tempo de execução. Para uso simples (uma sessão),
# o comportamento é seguro.
_cache_grade: pygame.Surface | None = None


def obter_fundo_grade() -> pygame.Surface:
    """Retorna superfície com grade de fundo (cacheada)."""
    global _cache_grade
    if _cache_grade is not None:
        return _cache_grade
    largura = COLUNAS * TAMANHO_CELULA
    altura = LINHAS * TAMANHO_CELULA
    superficie = pygame.Surface((largura, altura))
    superficie.fill(COR_FUNDO)
    for x in range(0, largura, 8):
        pygame.draw.line(superficie, COR_GRADE, (x, 0), (x, altura))
    for y in range(0, altura, 8):
        pygame.draw.line(superficie, COR_GRADE, (0, y), (largura, y))
    _cache_grade = superficie
    return _cache_grade


def _celula_aberta(mapa, coluna, linha, delta_col, delta_lin):
    """Indica se o vizinho na direção dada é corredor (não parede)."""
    linhas, colunas = len(mapa), len(mapa[0])
    nova_col, nova_lin = coluna + delta_col, linha + delta_lin
    if nova_lin < 0 or nova_lin >= linhas:
        return True
    if nova_col < 0 or nova_col >= colunas:
        return True
    return mapa[nova_lin][nova_col] != 1


def desenhar_parede_circuito(tela, mapa, coluna: int, linha: int):
    """Desenha trilhas de circuito na célula de parede indicada."""
    if mapa[linha][coluna] != 1:
        return
    x = coluna * TAMANHO_CELULA
    y = linha * TAMANHO_CELULA + OFFSET_Y
    espessura = 3
    if _celula_aberta(mapa, coluna, linha, 0, -1):
        pygame.draw.line(tela, COR_PAREDE, (x, y + espessura), (x + TAMANHO_CELULA, y + espessura), espessura)
    if _celula_aberta(mapa, coluna, linha, 0, 1):
        pygame.draw.line(tela, COR_PAREDE, (x, y + TAMANHO_CELULA - espessura),
                         (x + TAMANHO_CELULA, y + TAMANHO_CELULA - espessura), espessura)
    if _celula_aberta(mapa, coluna, linha, -1, 0):
        pygame.draw.line(tela, COR_PAREDE, (x + espessura, y), (x + espessura, y + TAMANHO_CELULA), espessura)
    if _celula_aberta(mapa, coluna, linha, 1, 0):
        pygame.draw.line(tela, COR_PAREDE, (x + TAMANHO_CELULA - espessura, y),
                         (x + TAMANHO_CELULA - espessura, y + TAMANHO_CELULA), espessura)


def _desenhar_no_rede(tela, centro_x: int, centro_y: int):
    """Desenha um nó luminoso de interseção no estilo circuito de rede."""
    pygame.draw.circle(tela, COR_PAREDE_BORDA, (centro_x, centro_y), 5, 1)
    pygame.draw.circle(tela, COR_PAREDE, (centro_x, centro_y), 3)
    pygame.draw.circle(tela, COR_NO, (centro_x, centro_y), 2)


def desenhar_nos_corredor(tela, mapa, posicoes_ignorar: set | None = None):
    """Desenha nós de rede em interseções, exceto nas posições ignoradas."""
    posicoes_ignorar = posicoes_ignorar or set()
    linhas, colunas = len(mapa), len(mapa[0])
    for linha in range(linhas):
        for coluna in range(colunas):
            if mapa[linha][coluna] == 1 or (coluna, linha) in posicoes_ignorar:
                continue
            vizinhos_abertos = sum(
                1 for dc, dl in ((0, -1), (0, 1), (-1, 0), (1, 0))
                if _celula_aberta(mapa, coluna, linha, dc, dl)
            )
            if vizinhos_abertos >= 3:
                cx = coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2
                cy = linha * TAMANHO_CELULA + TAMANHO_CELULA // 2 + OFFSET_Y
                _desenhar_no_rede(tela, cx, cy)
