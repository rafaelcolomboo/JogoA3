import pygame
"""Tela inicial do jogo."""
from utils.config import LARGURA, COR_AVATAR, COR_EMAIL, COR_TEXTO, COR_VPN, COR_EXPOS_LARAN


def desenhar_menu(tela, fonte_grande, fonte_media, fonte_pequena):
    itens = [
        (fonte_grande.render("DADOS NA REDE", True, COR_AVATAR), 165),
        (fonte_media.render("A3 - Exploracao Digital", True, COR_EMAIL), 205),
        (fonte_pequena.render("Coleta, armazenamento e uso de dados na internet",
                              True, (140, 140, 150)), 240),
        (fonte_grande.render("ENTER para jogar", True, COR_TEXTO), 350),
    ]
    for superficie, posicao_y in itens:
        tela.blit(superficie, (LARGURA // 2 - superficie.get_width() // 2, posicao_y))


def desenhar_tela_continuar(tela, fonte_grande, fonte_media, fonte_pequena, dicionario_sprites):

    titulo = fonte_grande.render("CONHEÇA AS AMEAÇAS", True, (255, 100, 100))
    tela.blit(titulo, (tela.get_width() // 2 - titulo.get_width() // 2, 50))

    pos_x_imagem = 100  
    pos_x_texto = 160  
    pos_y_inicial = 100
    espacamento = 80 

    ameacas = [
        ("Virus", "Código malicioso que infecta e corrompe seus dados.", (255, 150, 50), "Virus"), 
        ("Ransomware", "Criptografa seus arquivos.", (200, 50, 50), "Ransomware"),
        ("Spyware", "Monitora tudo o que você digita.", (150, 150, 255), "Spyware"),
        ("Hacker", "Invade seu sistema e te neutraliza.", (100, 150, 255), "Hacker")
    ]

    pos_y_atual = pos_y_inicial

    for nome, descricao, cor, chave_imagem in ameacas:
        
        # Tenta pegar a imagem do dicionário
        sprite_atual = dicionario_sprites.get(chave_imagem) 
        
        # Só desenha a imagem se ela existir (evita o jogo fechar se a chave estiver errada)
        if sprite_atual:
            tela.blit(sprite_atual, (pos_x_imagem, pos_y_atual))
        else:
            pygame.draw.circle(tela, cor, (pos_x_imagem + 15, pos_y_atual + 15), 15)     

        texto_nome = fonte_media.render(nome, True, cor)
        tela.blit(texto_nome, (pos_x_texto, pos_y_atual))

        texto_desc = fonte_pequena.render(descricao, True, (180, 180, 180))
        tela.blit(texto_desc, (pos_x_texto, pos_y_atual + 35))

        pos_y_atual += espacamento

    itens = [
        (fonte_grande.render("Setas ou WASD para mover", True, (110, 250, 120)), 460), 
        (fonte_media.render("# Colete VPN (escudo) para desconectar inimigos", True, (100, 200, 255)), 520), 
        (fonte_pequena.render("# Evite exposicao quando ameacas estiverem perto!", True, (255, 165, 0)), 540), 
        (fonte_pequena.render("# E-mail (+10) | Local (+30) | Banco (+50)", True, (100, 180, 100)), 560)
    ]
    
    for superficie, posicao_y in itens:
        tela.blit(superficie, (tela.get_width() // 2 - superficie.get_width() // 2, posicao_y))

    rodape = fonte_media.render("Aperte ENTER para iniciar a partida!", True, (255, 255, 255))
    tela.blit(rodape, (tela.get_width() // 2 - rodape.get_width() // 2, 620))