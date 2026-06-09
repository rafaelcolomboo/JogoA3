"""Loop principal e orquestração dos sistemas do jogo."""
import copy
import sys
import pygame
from utils.config import (
    LARGURA, ALTURA, FPS, MAPA_BASE, COR_FUNDO, COR_VERMELHO,
    DURACAO_VPN, PENALIDADE_MORTE, SPAWN_INIMIGOS,
)
from entities.jogador import Jogador
from entities.inimigo import Inimigo
from entities.dado import TipoDado
from entities.direcao import Direcao
from systems.carregador_sprites import carregar_sprites_inimigos, carregar_sprite_vpn
from systems.distribuicao_dados import criar_dados_do_mapa
from systems.exposicao import SistemaExposicao
from systems.colisao_inimigos import processar_colisoes
from systems.feedback import TextoFlutuante
from systems.render_cenario import desenhar_cenario
from systems.render_hud import desenhar_hud
from utils import arte_coletaveis
from scenes.tela_menu import desenhar_menu
from scenes.tela_menu import desenhar_tela_continuar
from scenes.tela_overlay import desenhar_overlay
from scenes.tela_resultado import desenhar_resultado_fase


class ControleJogo:
    """Gerencia estados, entrada, atualização e renderização do jogo."""

    def __init__(self):
        """Inicializa pygame, carrega assets e prepara a primeira partida."""
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Dados na Rede | A3 Exploracao Digital")
        self.relogio = pygame.time.Clock()
        self.fonte_grande = pygame.font.SysFont("consolas", 30, bold=True)
        self.fonte_media = pygame.font.SysFont("consolas", 17)
        self.fonte_pequena = pygame.font.SysFont("consolas", 14)
        self.sprites_inimigos = carregar_sprites_inimigos()
        self.sprites_coletaveis = self._montar_sprites_coletaveis()
        self.icone_vida = arte_coletaveis.criar_sprite_cadeado()
        self.sistema_exposicao = SistemaExposicao()
        self.estado = "MENU"
        self.atacante = ""
        self.fase = 1
        self.feedbacks: list[TextoFlutuante] = []
        self.estatisticas_fase: dict = {}
        self._iniciar_partida()

    def _montar_sprites_coletaveis(self) -> dict:
        return {
            TipoDado.EMAIL: arte_coletaveis.criar_sprite_email(),
            TipoDado.LOCALIZACAO: arte_coletaveis.criar_sprite_localizacao(),
            TipoDado.BANCARIO: arte_coletaveis.criar_sprite_bancario(),
            TipoDado.VPN: carregar_sprite_vpn(),
        }

    def _criar_inimigos(self) -> list[Inimigo]:
        inimigos = []
        for coluna, linha, nome, cor, icone in SPAWN_INIMIGOS:
            sprite = self.sprites_inimigos.get(nome)
            inimigos.append(Inimigo(coluna, linha, cor, nome, icone, sprite))
        return inimigos

    def _iniciar_partida(self):
        self.mapa = copy.deepcopy(MAPA_BASE)
        self.dados = criar_dados_do_mapa(self.sprites_coletaveis)
        self.jogador = Jogador(1, 1)
        self.jogador.estatisticas = {"email": 0, "localizacao": 0, "bancario": 0}
        self.inimigos = self._criar_inimigos()
        self.atacante = ""
        self.fase = 1
        self.feedbacks = []
        self.sistema_exposicao.resetar()

    def _contar_arquivos_restantes(self) -> int:
        return sum(1 for dado in self.dados if not dado.coletado)

    def _registrar_feedback(self, feedback):
        if feedback is None:
            return
        texto, cor, x, y = feedback
        self.feedbacks.append(TextoFlutuante(x, y, texto, cor))

    def _proxima_fase(self):
        self.fase += 1
        self.mapa = copy.deepcopy(MAPA_BASE)
        self.dados = criar_dados_do_mapa(self.sprites_coletaveis)
        self.jogador.resetar(1, 1)
        self.jogador.estatisticas = {"email": 0, "localizacao": 0, "bancario": 0}
        for inimigo in self.inimigos:
            inimigo.resetar()
        self.sistema_exposicao.resetar()
        self.feedbacks = []
        self.estado = "JOGANDO"

    def executar(self):
        """Inicia o loop principal até o jogador fechar a janela."""
        while True:
            self._processar_eventos()
            self._atualizar()
            self._renderizar()
            self.relogio.tick(FPS)

    def _processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type != pygame.KEYDOWN:
                continue
            self._tratar_tecla(evento.key)

    def _tratar_tecla(self, tecla):
        if self.estado == "MENU" and tecla == pygame.K_RETURN:
            self.estado = "TELA_CONTINUAR"
        elif self.estado == "TELA_CONTINUAR" and tecla == pygame.K_RETURN:
            self.estado = "JOGANDO"    
        elif self.estado == "JOGANDO" and tecla == pygame.K_ESCAPE:
            self.estado = "PAUSADO"
        elif self.estado == "PAUSADO" and tecla == pygame.K_ESCAPE:
            self.estado = "JOGANDO"
        elif self.estado =="PAUSADO" and tecla == pygame.K_m:
            self._iniciar_partida()
            self.estado = "MENU"    
        elif self.estado == "JOGANDO":
            self._aplicar_movimento_tecla(tecla)
        elif self.estado == "MORREU" and tecla == pygame.K_RETURN:
            self._continuar_apos_morte()
        elif self.estado == "RESULTADO_FASE" and tecla == pygame.K_RETURN:
            self._iniciar_partida()
            self.estado = "MENU"
        elif self.estado == "GAME_OVER" and tecla == pygame.K_RETURN:
            self._iniciar_partida()
            self.estado = "MENU"

    def _aplicar_movimento_tecla(self, tecla):
        teclas_direcao = {
            pygame.K_UP: Direcao.CIMA, pygame.K_DOWN: Direcao.BAIXO,
            pygame.K_LEFT: Direcao.ESQUERDA, pygame.K_RIGHT: Direcao.DIREITA,
            pygame.K_w: Direcao.CIMA, pygame.K_s: Direcao.BAIXO,
            pygame.K_a: Direcao.ESQUERDA, pygame.K_d: Direcao.DIREITA,
        }
        if tecla in teclas_direcao:
            self.jogador.definir_direcao(teclas_direcao[tecla])

    def _continuar_apos_morte(self):
        if self.jogador.vidas > 0:
            self.jogador.resetar(1, 1)
            for inimigo in self.inimigos:
                inimigo.resetar()
            self.sistema_exposicao.resetar()
            self.estado = "JOGANDO"
        else:
            self.estado = "GAME_OVER"

    def _atualizar(self):
        if self.estado != "JOGANDO":
            return
        self.jogador.atualizar(self.mapa)
        vpn_ativa, feedback = self.jogador.coletar(self.dados)
        self._registrar_feedback(feedback)
        if vpn_ativa:
            self.jogador.vpn_ativa = True
            self.jogador.tempo_inicio_vpn = 0
            for inimigo in self.inimigos:
                inimigo.assustar(DURACAO_VPN)
        if self.jogador.vpn_ativa:
            self.jogador.tempo_inicio_vpn += 1 
            if self.jogador.tempo_inicio_vpn >= self.jogador.duracao_vpn:
                self.jogador.vpn_ativa = False    

        # Barra de exposição sobe com inimigos próximos; 100% causa morte sem colisão física
        if self._atualizar_exposicao():
            return
        # Colisão com malware: neutraliza se VPN ativa, senão perde vida
        if self._atualizar_colisoes():
            return
        self.feedbacks = [fb for fb in self.feedbacks if fb.atualizar()]
        if self._contar_arquivos_restantes() == 0:
            self.estatisticas_fase = dict(self.jogador.estatisticas)
            self.estado = "RESULTADO_FASE"

    def _atualizar_exposicao(self) -> bool:
        resultado = self.sistema_exposicao.atualizar(self.jogador, self.inimigos)
        if resultado != "MORREU":
            return False
        self.atacante = self.sistema_exposicao.mensagem_morte()
        self.estado = "MORREU"
        return True

    def _atualizar_colisoes(self) -> bool:
        for inimigo in self.inimigos:
            inimigo.atualizar(self.mapa, self.jogador.x, self.jogador.y)
        novo_estado, atacante, feedback = processar_colisoes(self.jogador, self.inimigos)
        self._registrar_feedback(feedback)
        if novo_estado is None:
            return False
        self.atacante = atacante
        self.estado = novo_estado
        return True

    def _renderizar(self):
        self.tela.fill(COR_FUNDO)
        if self.estado == "MENU":
            desenhar_menu(self.tela, self.fonte_grande, self.fonte_media, self.fonte_pequena)

        elif self.estado == "TELA_CONTINUAR":
            desenhar_tela_continuar(self.tela, self.fonte_grande, self.fonte_media, self.fonte_pequena, self.sprites_inimigos)

        elif self.estado in ["JOGANDO", "PAUSADO", "MORREU", "GAME_OVER", "RESULTADO_FASE", "TELA_CONTINUAR"]:
            self._renderizar_partida()

        if self.estado == "PAUSADO":
            desenhar_overlay(self.tela, self.fonte_grande, self.fonte_media, self.fonte_pequena,
                            "JOGO PAUSADO!", COR_VERMELHO,
                            f"Dados Coletados no Momento: {self.jogador.pontuacao}",
                            "Pressione ESC para retomar o jogo | Ou (M) para voltar ao MENU!",
                             )
        pygame.display.flip()

                        
    def _renderizar_partida(self):
        desenhar_cenario(self.tela, self.mapa, self.dados, self.inimigos)
        for dado in self.dados:
            dado.desenhar(self.tela)
        self.jogador.desenhar(self.tela)
        for inimigo in self.inimigos:
            inimigo.desenhar(self.tela)
        for feedback in self.feedbacks:
            feedback.desenhar(self.tela)
        desenhar_hud(self.tela, self.fonte_media, self.fonte_pequena, self.jogador,
                     self._contar_arquivos_restantes(), self.sistema_exposicao.nivel,
                     self.fase, self.icone_vida)
        self._renderizar_overlay_estado()

    def _renderizar_overlay_estado(self):
        if self.estado == "MORREU":
            titulo = "DADO VAZADO!" if "Exposicao" in self.atacante else "VOCE FOI ATACADO!"
            desenhar_overlay(self.tela, self.fonte_grande, self.fonte_media, self.fonte_pequena,
                             titulo, COR_VERMELHO,
                             f"{self.atacante}  |  -{PENALIDADE_MORTE} pts",
                             "ENTER para continuar")
        elif self.estado == "RESULTADO_FASE":
            desenhar_resultado_fase(self.tela, self.fonte_grande, self.fonte_media,
                                    self.fonte_pequena, self.fase,
                                    self.estatisticas_fase, self.jogador.pontuacao)
        elif self.estado == "GAME_OVER":
            desenhar_overlay(self.tela, self.fonte_grande, self.fonte_media, self.fonte_pequena,
                             "GAME OVER", COR_VERMELHO,
                             f"Dados coletados: {self.jogador.pontuacao}",
                             "ENTER para voltar ao menu")
