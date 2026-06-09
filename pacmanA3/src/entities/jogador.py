"""Entidade do usuário navegando na rede (antigo Pac-Man)."""
import math
import pygame
from src.utils.config import TAMANHO_CELULA, COLUNAS, OFFSET_Y, TAMANHO_AVATAR, DURACAO_VPN, COR_ESCUDO
from src.entities.direcao import Direcao
from src.entities.dado import TipoDado
from src.utils.arte_jogador import criar_animacao_jogador


class Jogador:
    """Controla movimento, coleta de dados, escudo VPN e pontuação."""

    VELOCIDADE = 3

    def __init__(self, coluna: int, linha: int):
        """
        Args:
            coluna: Posição inicial na grade (eixo horizontal).
            linha: Posição inicial na grade (eixo vertical).
        """
        self.coluna = coluna
        self.linha = linha
        self.x = float(coluna * TAMANHO_CELULA)
        self.y = float(linha * TAMANHO_CELULA)
        self.direcao = Direcao.PARADO
        self.proxima_direcao = Direcao.PARADO
        self.pontuacao = 0
        self.vidas = 3
        self.timer_escudo = 0
        self.estatisticas = {"email": 0, "localizacao": 0, "bancario": 0}
        self._animacao = criar_animacao_jogador()
        self._quadro_animacao = 0
        self._contador_animacao = 0
        self.vpn_ativa = False
        self.tempo_inicio_vpn = 0
        self.duracao_vpn = 480
     
    @property
    def rect(self) -> pygame.Rect:
        margem = (TAMANHO_CELULA - TAMANHO_AVATAR) // 2
        return pygame.Rect(
            int(self.x) + margem, int(self.y) + margem + OFFSET_Y,
            TAMANHO_AVATAR, TAMANHO_AVATAR,
        )

    def definir_direcao(self, direcao: Direcao):
        """Armazena a próxima direção desejada pelo jogador."""
        self.proxima_direcao = direcao

    def _pode_mover_para(self, mapa, coluna, linha) -> bool:
        if linha < 0 or linha >= len(mapa):
            return False
        return mapa[linha][coluna % COLUNAS] != 1

    def _alinhar_na_grade(self, mapa):
        """Ajusta direção quando o jogador está alinhado ao centro da célula."""
        coluna = int(self.x // TAMANHO_CELULA)
        linha = int(self.y // TAMANHO_CELULA)
        offset_x = self.x - coluna * TAMANHO_CELULA
        offset_y = self.y - linha * TAMANHO_CELULA
        if abs(offset_x) >= self.VELOCIDADE or abs(offset_y) >= self.VELOCIDADE:
            return
        delta_col, delta_lin = self.proxima_direcao.value
        if self._pode_mover_para(mapa, coluna + delta_col, linha + delta_lin):
            self.direcao = self.proxima_direcao
        delta_col, delta_lin = self.direcao.value
        if not self._pode_mover_para(mapa, coluna + delta_col, linha + delta_lin):
            self.direcao = Direcao.PARADO

    def _aplicar_movimento(self, mapa):
        """Move o jogador na direção atual, respeitando paredes e túnel lateral."""
        delta_col, delta_lin = self.direcao.value
        novo_x = self.x + delta_col * self.VELOCIDADE
        novo_y = self.y + delta_lin * self.VELOCIDADE
        nova_coluna = int(novo_x // TAMANHO_CELULA) % COLUNAS
        nova_linha = int(novo_y // TAMANHO_CELULA)
        if self._pode_mover_para(mapa, nova_coluna, nova_linha):
            self.x = novo_x % (COLUNAS * TAMANHO_CELULA)
            self.y = novo_y

    def _atualizar_animacao(self):
        if self.direcao != Direcao.PARADO:
            self._contador_animacao += 1
            if self._contador_animacao >= 8:
                self._contador_animacao = 0
                self._quadro_animacao = (self._quadro_animacao + 1) % 3
        else:
            self._quadro_animacao = 0

    def atualizar(self, mapa):
        """Atualiza posição, animação e timer do escudo VPN."""
        self._alinhar_na_grade(mapa)
        self._aplicar_movimento(mapa)
        self._atualizar_animacao()
        if self.timer_escudo > 0:
            self.timer_escudo -= 1

        if self.vpn_ativa:
            if self.tempo_inicio_vpn >= self.duracao_vpn:
                self.vpn_ativa = False  
                 

    def coletar(self, dados: list) -> tuple[bool, tuple | None]:
        """
        Verifica colisão com coletáveis.

        Returns:
            Tupla (ativou_vpn, feedback) onde feedback é (texto, cor, x, y) ou None.
        """
        for dado in dados:
            if dado.coletado:
                continue
            delta_x = dado.coluna * TAMANHO_CELULA + TAMANHO_CELULA // 2 - self.rect.centerx
            delta_y = (dado.linha * TAMANHO_CELULA + TAMANHO_CELULA // 2
                       + OFFSET_Y - self.rect.centery)
            if math.hypot(delta_x, delta_y) < TAMANHO_CELULA // 2:
                dado.coletado = True
                self.pontuacao += dado.valor
                feedback = (dado.feedback, dado.cor_feedback + (255,),
                            self.rect.centerx, self.rect.centery)
                if dado.tipo == TipoDado.VPN:
                    self.vpn_ativa = True 
                    self.tempo_inicio_vpn = 0
                    self.timer_escudo = DURACAO_VPN
                    return True, feedback
                self.estatisticas[dado.tipo.value] += 1
                return False, feedback
        return False, None

    def resetar(self, coluna: int, linha: int):
        """Reposiciona o jogador após morte ou nova fase."""
        self.coluna = coluna
        self.linha = linha
        self.x = float(coluna * TAMANHO_CELULA)
        self.y = float(linha * TAMANHO_CELULA)
        self.direcao = Direcao.PARADO
        self.proxima_direcao = Direcao.PARADO

    def desenhar(self, tela: pygame.Surface):
        """Desenha avatar animado e borda do escudo VPN quando ativo."""
        centro_x = int(self.x) + TAMANHO_CELULA // 2
        centro_y = int(self.y) + TAMANHO_CELULA // 2 + OFFSET_Y
        direcao = self.direcao if self.direcao != Direcao.PARADO else Direcao.DIREITA
        sprite = self._animacao[direcao][self._quadro_animacao]
        tela.blit(sprite, sprite.get_rect(center=(centro_x, centro_y)))
        if self.timer_escudo > 0:
            pulso = 3 + int(2 * math.sin(self.timer_escudo * 0.2))
            pygame.draw.circle(tela, COR_ESCUDO, (centro_x, centro_y),
                               TAMANHO_AVATAR // 2 + pulso, 2)
