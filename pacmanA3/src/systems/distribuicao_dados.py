"""Criação e distribuição dos coletáveis no mapa."""
import random
from entities.dado import Dado, TipoDado
from utils.config import MAPA_BASE, FREQ_LOCAL, FREQ_BANCO


def distribuir_tipos(posicoes: list) -> list[TipoDado]:
    """
    Define tipo de cada célula de dado comum.

    Args:
        posicoes: Lista de coordenadas (coluna, linha) com valor 2 no mapa.

    Returns:
        Lista de TipoDado na mesma ordem de posicoes.
    """
    quantidade = len(posicoes)
    qtd_banco = max(1, quantidade // FREQ_BANCO)
    qtd_local = max(1, quantidade // FREQ_LOCAL)
    qtd_banco = min(qtd_banco, max(1, quantidade // 8))
    qtd_local = min(qtd_local, max(1, quantidade // 4))
    if qtd_banco + qtd_local >= quantidade:
        qtd_banco = max(1, quantidade // 15)
        qtd_local = max(1, quantidade // 5)
    tipos = [TipoDado.EMAIL] * quantidade
    indices = list(range(quantidade))
    random.shuffle(indices)
    for indice in indices[:qtd_banco]:
        tipos[indice] = TipoDado.BANCARIO
    restantes = [i for i in indices[qtd_banco:] if tipos[i] == TipoDado.EMAIL]
    random.shuffle(restantes)
    for indice in restantes[:qtd_local]:
        tipos[indice] = TipoDado.LOCALIZACAO
    return tipos


def criar_dados_do_mapa(sprites_por_tipo: dict) -> list[Dado]:
    """
    Instancia todos os coletáveis conforme MAPA_BASE.

    Args:
        sprites_por_tipo: Dicionário TipoDado -> pygame.Surface.

    Returns:
        Lista de objetos Dado posicionados no labirinto.
    """
    posicoes_normais = []
    posicoes_vpn = []
    for linha, linha_mapa in enumerate(MAPA_BASE):
        for coluna, celula in enumerate(linha_mapa):
            if celula == 2:
                posicoes_normais.append((coluna, linha))
            elif celula == 3:
                posicoes_vpn.append((coluna, linha))
    tipos = distribuir_tipos(posicoes_normais)
    dados = [
        Dado(coluna, linha, tipo, sprites_por_tipo[tipo])
        for (coluna, linha), tipo in zip(posicoes_normais, tipos)
    ]
    for coluna, linha in posicoes_vpn:
        dados.append(Dado(coluna, linha, TipoDado.VPN, sprites_por_tipo[TipoDado.VPN]))
    return dados
