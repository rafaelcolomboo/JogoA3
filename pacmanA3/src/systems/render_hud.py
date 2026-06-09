"""Painel superior: pontuação, arquivos, exposição e vidas."""
import pygame
from utils.config import (
    LARGURA, COR_TEXTO, COR_EMAIL, COR_EXPOS_VERDE,
    COR_EXPOS_LARAN, COR_EXPOS_VERM,
)

def _cor_barra_exposicao(nivel: float) -> tuple:
    """Retorna cor RGB da barra conforme faixa de risco (verde, laranja ou vermelho)."""
    if nivel <= 50:
        return COR_EXPOS_VERDE
    if nivel <= 80:
        return COR_EXPOS_LARAN
    return COR_EXPOS_VERM


def desenhar_hud(tela, fonte_media, fonte_pequena, jogador, arquivos_restantes,
                 nivel_exposicao: float, fase: int, icone_vida):
    """Desenha HUD completo na parte superior da tela."""
    posicao_y = 8
    texto_pontos = fonte_media.render(
        f"DADOS COLETADOS: {jogador.pontuacao:05d}", True, COR_TEXTO)
    texto_arquivos = fonte_media.render(
        f"ARQUIVOS: {arquivos_restantes:03d}", True, COR_EMAIL)
    texto_exposicao = fonte_pequena.render("EXPOSICAO:", True, COR_TEXTO)
    tela.blit(texto_pontos, (10, posicao_y))
    tela.blit(texto_arquivos, (10, posicao_y + 24))
    tela.blit(texto_exposicao, (10, posicao_y + 48))
    _desenhar_barra_exposicao(tela, fonte_pequena, posicao_y + 48, nivel_exposicao)
    texto_fase = fonte_pequena.render(f"FASE {fase}", True, (120, 120, 140))
    tela.blit(texto_fase, (LARGURA // 2 - texto_fase.get_width() // 2, posicao_y + 70))
    _desenhar_vidas(tela, jogador.vidas, icone_vida, posicao_y)
        
    if jogador.vpn_ativa:
        frames_restantes = max(0, jogador.duracao_vpn - jogador.tempo_inicio_vpn)
        porcentagem = frames_restantes / jogador.duracao_vpn

        largura_maxima = 200
        altura_barra = 20
        pos_x = tela.get_width() // 2 - largura_maxima // 2
        pos_y = tela.get_height() - 30

        # Desenha Fundo Cinza
        pygame.draw.rect(tela, (60, 60, 60), (pos_x, pos_y, largura_maxima, altura_barra))

        # Define a cor (Verde, mudando para Vermelho nos últimos 25%)
        cor_liquido = (50, 200, 100)
        if porcentagem <= 0.25:
            cor_liquido = (255, 50, 50)

        # Desenha a barra encolhendo da direita para a esquerda
        largura_atual = largura_maxima * porcentagem
        pygame.draw.rect(tela, cor_liquido, (pos_x, pos_y, largura_atual, altura_barra))

        # Texto descritivo
        texto_vpn = fonte_pequena.render("VPN:", True, (255, 255, 255))
        tela.blit(texto_vpn, (pos_x - 50, pos_y))

        # Texto
        texto_vpn = fonte_pequena.render("VPN:", True, (255, 255, 255))
        tela.blit(texto_vpn, (pos_x - 50, pos_y))

def _desenhar_barra_exposicao(tela, fonte, posicao_y, nivel):
    """Renderiza barra de progresso e percentual de exposição de dados."""
    barra_x, barra_y, largura, altura = 120, posicao_y, 200, 14
    pygame.draw.rect(tela, (30, 30, 40), (barra_x, barra_y, largura, altura), border_radius=4)
    preenchimento = int(largura * nivel / 100)
    if preenchimento > 0:
        pygame.draw.rect(tela, _cor_barra_exposicao(nivel),
                         (barra_x, barra_y, preenchimento, altura), border_radius=4)
    texto_pct = fonte.render(f"{int(nivel)}%", True, COR_TEXTO)
    tela.blit(texto_pct, (barra_x + largura + 8, barra_y - 1))


def _desenhar_vidas(tela, vidas, icone, posicao_y):
    """Exibe ícones de cadeado no canto superior direito (vidas restantes)."""
    for indice in range(vidas):
        tela.blit(icone, (LARGURA - 24 - indice * 22, posicao_y + 4))
