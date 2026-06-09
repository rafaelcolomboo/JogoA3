"""Constantes globais do jogo: cores, mapa, pontuação e caminhos de assets."""
import os

PASTA_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _resolver_pasta(*candidatos: str) -> str:
    """Retorna a primeira pasta existente entre os caminhos candidatos."""
    for partes in candidatos:
        caminho = os.path.join(PASTA_RAIZ, *partes.split("/"))
        if os.path.isdir(caminho):
            return caminho
    return os.path.join(PASTA_RAIZ, *candidatos[0].split("/"))


PASTA_INIMIGOS = _resolver_pasta("assets/sprites/inimigos", "assets/inimigos")
PASTA_DADOS = _resolver_pasta("assets/sprites/dados", "assets/dados")

IMAGENS_INIMIGOS = {
    "Virus": "virus.png",
    "Spyware": "spyware.png",
    "Ransomware": "ransomware.png",
    "Hacker": "hacker.png",
}
IMAGEM_VPN = "powerup.png"

LARGURA = 560
ALTURA = 720
TAMANHO_CELULA = 40
COLUNAS = LARGURA // TAMANHO_CELULA
OFFSET_Y = 110
FPS = 60
PENALIDADE_MORTE = 100

COR_FUNDO = (10, 10, 15)
COR_GRADE = (13, 43, 13)
COR_PAREDE = (26, 46, 255)
COR_PAREDE_BORDA = (61, 90, 254)
COR_NO = (0, 255, 65)
COR_TEXTO = (255, 255, 255)
COR_AVATAR = (0, 207, 255)
COR_EMAIL = (0, 255, 65)
COR_LOCAL = (255, 140, 0)
COR_BANCO = (255, 215, 0)
COR_VPN = (0, 255, 65)
COR_ESCUDO = (100, 255, 200)
COR_EXPOS_VERDE = (0, 255, 65)
COR_EXPOS_LARAN = (255, 140, 0)
COR_EXPOS_VERM = (255, 45, 45)
COR_CADEADO = (0, 255, 65)
COR_VERMELHO = (220, 50, 50)
COR_ROSA = (255, 100, 180)
COR_CIANO = (0, 220, 220)
COR_LARANJA = (255, 150, 0)

TAMANHO_SPRITE_INIMIGO = 40
TAMANHO_HITBOX_INIMIGO = 26
TAMANHO_AVATAR = 32
DURACAO_VPN = FPS * 8
DURACAO_FEEDBACK = 50
DISTANCIA_EXPOSICAO = 3
TAXA_EXPOS_SOBE = 0.55
TAXA_EXPOS_DESCE = 0.12

VALOR_EMAIL = 10
VALOR_LOCAL = 30
VALOR_BANCO = 50
FREQ_LOCAL = 5
FREQ_BANCO = 15

MSG_EDUCATIVA = {
    "email": "Seu e-mail é usado para rastrear seu comportamento online.",
    "localizacao": "Apps coletam sua localização mesmo quando não estão em uso.",
    "bancario": "Dados financeiros são os mais visados por ransomware.",
}

SPAWN_INIMIGOS = [
    (6, 5, "Virus", COR_VERMELHO, "V"),
    (7, 5, "Spyware", COR_ROSA, "S"),
    (6, 6, "Ransomware", COR_CIANO, "R"),
    (7, 6, "Hacker", COR_LARANJA, "H"),
]

MAPA_BASE = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],    # 1 = parede, 2 = dados, 3 = power-up (vpn), 0 = espaço vazio (spawn)
    [1, 2, 2, 2, 2, 2, 1, 1, 2, 2, 2, 2, 2, 1],
    [1, 3, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 3, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 0, 0, 1, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 0, 0, 0, 0, 2, 2, 2, 2, 1],
    [1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 2, 1],
    [1, 2, 1, 1, 2, 2, 2, 2, 2, 2, 1, 1, 2, 1],
    [1, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 1],
    [1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1],
    [1, 2, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 2, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
LINHAS = len(MAPA_BASE)
