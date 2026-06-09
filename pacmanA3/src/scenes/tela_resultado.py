"""Tela educativa ao concluir uma fase."""
import pygame
from utils.config import (
    LARGURA, ALTURA, COR_AVATAR, COR_EMAIL, COR_LARANJA, COR_TEXTO, COR_VPN, MSG_EDUCATIVA,
)


def _tipo_mais_coletado(estatisticas: dict) -> str:
    if not any(estatisticas.values()):
        return "email"
    return max(estatisticas, key=estatisticas.get)


def desenhar_resultado_fase(tela, fonte_grande, fonte_media, fonte_pequena,
                            fase: int, estatisticas: dict, pontuacao_total: int):
    """Exibe totais coletados e mensagem educativa da fase."""
    camada = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
    camada.fill((0, 0, 0, 200))
    tela.blit(camada, (0, 0))
    titulo = fonte_grande.render("VITÓRIA", True, COR_AVATAR)
    tela.blit(titulo, (LARGURA // 2 - titulo.get_width() // 2, 90))
    linhas = [
        (f"E-mails coletados:        {estatisticas.get('email', 0)}", COR_EMAIL),
        (f"Localizacoes coletadas:   {estatisticas.get('localizacao', 0)}", COR_LARANJA),
        (f"Dados bancarios:          {estatisticas.get('bancario', 0)}", (255, 215, 0)),
        (f"Total de dados:           {pontuacao_total}", COR_TEXTO),
    ]
    posicao_y = 160
    for texto, cor in linhas:
        superficie = fonte_media.render(texto, True, cor)
        tela.blit(superficie, (LARGURA // 2 - superficie.get_width() // 2, posicao_y))
        posicao_y += 32
    _desenhar_caixa_educativa(tela, fonte_pequena, posicao_y, estatisticas)
    botao = fonte_media.render("ENTER - Voltar ao menu", True, COR_VPN)
    tela.blit(botao, (LARGURA // 2 - botao.get_width() // 2, ALTURA - 80))


def _desenhar_caixa_educativa(tela, fonte, posicao_y, estatisticas):
    tipo = _tipo_mais_coletado(estatisticas)
    mensagem = MSG_EDUCATIVA[tipo]
    caixa = pygame.Rect(40, posicao_y + 10, LARGURA - 80, 70)
    pygame.draw.rect(tela, (20, 40, 30), caixa, border_radius=8)
    pygame.draw.rect(tela, COR_EMAIL, caixa, 2, border_radius=8)
    texto = fonte.render(mensagem, True, COR_TEXTO)
    tela.blit(texto, (caixa.x + 12, caixa.centery - texto.get_height() // 2))
