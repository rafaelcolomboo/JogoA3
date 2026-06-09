"""Desenho do labirinto e fundo."""
from utils.config import LINHAS, COLUNAS, OFFSET_Y
from utils.arte_cenario import obter_fundo_grade, desenhar_parede_circuito, desenhar_nos_corredor


def desenhar_cenario(tela, mapa, dados, inimigos):
    """
    Renderiza grade, paredes em estilo circuito e nós de rede.

    Args:
        tela: Superfície principal do pygame.
        mapa: Matriz do labirinto.
        dados: Lista de coletáveis (para ignorar nós no chão).
        inimigos: Lista de inimigos (para ignorar spawn).
    """
    tela.blit(obter_fundo_grade(), (0, OFFSET_Y))
    for linha in range(LINHAS):
        for coluna in range(COLUNAS):
            if mapa[linha][coluna] == 1:
                desenhar_parede_circuito(tela, mapa, coluna, linha)
    posicoes_ignorar = {(dado.coluna, dado.linha) for dado in dados}
    posicoes_ignorar |= {(ini.spawn_coluna, ini.spawn_linha) for ini in inimigos}
    desenhar_nos_corredor(tela, mapa, posicoes_ignorar)
