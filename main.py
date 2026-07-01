import pygame
import recursos
import config
import render
import sys
from jogador import Jogador
from inimigo import Inimigo
import random
import math

class ItemColetavel:
    def __init__(self, tipo, x, y):
        self.tipo = tipo # 'vida', 'energia' ou 'escudo'
        if tipo == 'vida':
            self.image = recursos.item_vida_img
        elif tipo == 'energia':
            self.image = recursos.item_energia_img
        elif tipo == 'escudo':
            self.image = recursos.item_escudo_img
        self.rect = self.image.get_rect(center=(x, y))

pygame.init()

# =========================================================================
# CONFIGURAÇÃO DA TELA ADAPTÁVEL (SISTEMA DE SUPERFÍCIE VIRTUAL)
# =========================================================================
LARGURA_VIRTUAL = 1920
ALTURA_VIRTUAL = 1080
superficie_virtual = pygame.Surface((LARGURA_VIRTUAL, ALTURA_VIRTUAL))

# Tamanho inicial da janela (pode ser esticada ou maximizada pelo usuário)
largura_janela_real = 1280
altura_janela_real = 720
tela_real = pygame.display.set_mode((largura_janela_real, altura_janela_real), pygame.RESIZABLE)
pygame.display.set_caption("Cin Adventure")

largura_calculada = recursos.inicializar_recursos((LARGURA_VIRTUAL, ALTURA_VIRTUAL), config.ALTURA_PERSONAGEM)
jogador = Jogador(largura_calculada)

# Carrega a imagem do crachá para ser usada no spawn e HUD
try:
    img_cracha_original = pygame.image.load("png dos sprites/objeto cracha.png").convert_alpha()
    img_cracha = pygame.transform.scale(img_cracha_original, (55, 55))
    img_cracha_hud = pygame.transform.scale(img_cracha_original, (35, 35))
except Exception as e:
    print(e)
    img_cracha = pygame.Surface((55, 55))
    img_cracha.fill((255, 215, 0))
    img_cracha_hud = pygame.transform.scale(img_cracha, (35, 35))

# Posicionamento do NPC
rect_npc1 = pygame.Rect(450, config.chao.y - 128, 64, 64)

config.ultimo_tempo = pygame.time.get_ticks()
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 20)
fonte_hud_cracha = pygame.font.SysFont("Arial", 28, bold=True)

config.tempo_descanso_inimigo = 0
config.game_over = False

# Inicializa variáveis extras de controle de itens caso não existam no config
if not hasattr(config, 'velocidade_aumentada'):
    config.velocidade_aumentada = False
if not hasattr(config, 'tempo_escudo_restante'):
    config.tempo_escudo_restante = 0
if not hasattr(config, 'tempo_energia_restante'):
    config.tempo_energia_restante = 0
if not hasattr(config, 'cooldown_tiro_reduzido'):
    config.cooldown_tiro_reduzido = False
if not hasattr(config, 'itens_no_chao'):
    config.itens_no_chao = []
if not hasattr(config, 'inventario'):
    config.inventario = {"vida": 0, "energia": 0, "escudo": 0, "cracha": 0}
elif "cracha" not in config.inventario:
    config.inventario["cracha"] = 0
if not hasattr(config, 'crachas_gerados_na_fase'):
    config.crachas_gerados_na_fase = False

config.carregar_fase(0)

def reiniciar_jogo():
    # Reseta a vida do jogador
    jogador.vida_atual = jogador.vida_maxima
    jogador.em_hit = False
    jogador.invulneravel = 0
    
    # Reseta estados do jogo e pontuação
    config.game_over = False
    config.score = 0  # ZERA O SCORE
    config.tempo_descanso_inimigo = 0
    
    # Reseta efeitos de itens ativos
    config.velocidade_aumentada = False
    config.tempo_escudo_restante = 0
    config.tempo_energia_restante = 0
    config.cooldown_tiro_reduzido = False
    jogador.velocidade = 5
    # Limpa projéteis e drops do chão
    config.projeteis.clear()
    config.itens_no_chao.clear()
    
    # ZERA O INVENTÁRIO COMPLETAMENTE
    config.inventario = {"vida": 0, "energia": 0, "escudo": 0, "cracha": 0}
    config.crachas_gerados_na_fase = False
    
    # VOLTA PARA O COMEÇO 
    config.fase_atual = 0
    jogador.rect.x = config.POS_X_INICIAL
    jogador.rect.y = config.POS_Y_INICIAL
    jogador.velocidade_y = 0
    
    # Recarrega o mapa inicial
    config.carregar_fase(0)

def usar_vida():
    if config.inventario["vida"] > 0:
        if jogador.vida_atual < jogador.vida_maxima:
            config.inventario["vida"] -= 1
            jogador.vida_atual += 1

def usar_energia():
    if config.inventario["energia"] > 0:
        config.inventario["energia"] -= 1
        config.tempo_energia_restante = 600
        config.cooldown_tiro_reduzido = True
        jogador.velocidade = 10

def usar_escudo():
    if config.inventario["escudo"] > 0:
        config.inventario["escudo"] -= 1
        config.tempo_escudo_restante = 600

pause_selecionado = 0
jogo_pausado = False
mostrar_controles_pause = False

menu_selecionado = 0
mostrar_controles = False

config.no_menu = True

# LOOP PRINCIPAL DO JOGO
while config.rodando:
    clock.tick(60)
    tempo_atual = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed()
    
    config.plataformas = config.fases[config.fase_atual].atualizar_plataformas(jogador.rect, jogador.pulando)
    
    if config.tempo_escudo_restante > 0:
        config.tempo_escudo_restante -= 1
    if config.tempo_energia_restante > 0:
        config.tempo_energia_restante -= 1
        config.velocidade_aumentada = True
        config.cooldown_tiro_reduzido = True
        jogador.velocidade = 10
    else:
        config.tempo_energia_restante = 0
        config.velocidade_aumentada = False
        config.cooldown_tiro_reduzido = False
        jogador.velocidade = 5

    # =========================================================================
    # ESTADO 1: MENU INICIAL
    # =========================================================================
    if config.no_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            elif evento.type == pygame.VIDEORESIZE:
                largura_janela_real, altura_janela_real = evento.w, evento.h
                tela_real = pygame.display.set_mode((largura_janela_real, altura_janela_real), pygame.RESIZABLE)
                
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrar_controles = False
                if mostrar_controles:
                    if evento.key == pygame.K_SPACE:
                        mostrar_controles = False
                else:
                    if evento.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selecionado = (menu_selecionado + 1) % 3
                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        menu_selecionado = (menu_selecionado - 1) % 3
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if menu_selecionado == 0:
                            config.no_menu = False
                        elif menu_selecionado == 1:
                            mostrar_controles = True
                        elif menu_selecionado == 2:
                            config.rodando = False

        render.desenhar_menu(superficie_virtual, menu_selecionado, mostrar_controles)
        tela_redimensionada = pygame.transform.scale(superficie_virtual, (largura_janela_real, altura_janela_real))
        tela_real.blit(tela_redimensionada, (0, 0))
        pygame.display.flip()
        continue

    # =========================================================================
    # ESTADO 2: GAME OVER
    # =========================================================================
    if config.game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            elif evento.type == pygame.VIDEORESIZE:
                largura_janela_real, altura_janela_real = evento.w, evento.h
                tela_real = pygame.display.set_mode((largura_janela_real, altura_janela_real), pygame.RESIZABLE)
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_jogo()

        superficie_virtual.blit(recursos.sprite_tela_game_over, (0,0))
        cor_do_texto = (240, 240, 220)
        texto_instrucao = recursos.fonte_game_over.render("PRESSIONE ESPACO PARA TENTAR NOVAMENTE", True, cor_do_texto)
        superficie_virtual.blit(texto_instrucao, (565, 780))
        
        tela_redimensionada = pygame.transform.scale(superficie_virtual, (largura_janela_real, altura_janela_real))
        tela_real.blit(tela_redimensionada, (0, 0))
        pygame.display.flip()
        continue

    # =========================================================================
    # ESTADO 3: EVENTOS DO JOGO (Normal e Pausado)
    # =========================================================================
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            config.rodando = False
        elif evento.type == pygame.VIDEORESIZE:
            largura_janela_real, altura_janela_real = evento.w, evento.h
            tela_real = pygame.display.set_mode((largura_janela_real, altura_janela_real), pygame.RESIZABLE)

        if evento.type == pygame.KEYDOWN:
            # --- SE O JOGO ESTIVER PAUSADO ---
            if jogo_pausado:
                if mostrar_controles_pause:
                    if evento.key in (pygame.K_ESCAPE, pygame.K_SPACE, pygame.K_RETURN):
                        mostrar_controles_pause = False
                else:
                    if evento.key == pygame.K_ESCAPE:
                        jogo_pausado = False
                    elif evento.key in (pygame.K_DOWN, pygame.K_s):
                        pause_selecionado = (pause_selecionado + 1) % 4
                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        pause_selecionado = (pause_selecionado - 1) % 4
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if pause_selecionado == 0:
                            jogo_pausado = False
                        elif pause_selecionado == 1:
                            config.carregar_fase(config.fase_atual)
                            config.projeteis.clear()
                            config.itens_no_chao.clear()
                            jogador.rect.x = config.POS_X_INICIAL
                            jogador.rect.y = config.POS_Y_INICIAL
                            jogo_pausado = False
                        elif pause_selecionado == 2:
                            mostrar_controles_pause = True
                        elif pause_selecionado == 3:
                            config.rodando = False
            # --- SE O JOGO ESTIVER RODANDO NORMALMENTE ---
            else:
                if evento.key == pygame.K_ESCAPE:
                    jogo_pausado = True
                    pause_selecionado = 0
                    mostrar_controles_pause = False
                elif evento.key == pygame.K_SPACE and not jogador.pulando and not jogador.em_hit:
                    jogador.pulando = True
                    jogador.velocidade_y = -config.velocidade_pulo
                elif evento.key == pygame.K_UP and not jogador.pulando and not jogador.em_hit:
                    jogador.pulando = True
                    jogador.velocidade_y = -config.velocidade_pulo
                elif evento.key == pygame.K_k:
                    config.atacando
                elif evento.key == pygame.K_1:
                    usar_vida()
                elif evento.key == pygame.K_2:
                    usar_energia()
                elif evento.key == pygame.K_3:
                    usar_escudo()
                elif evento.key == pygame.K_t:
                    if config.perto_do_npc and config.fase_atual == 0:
                        if not config.mostrar_balao:
                            config.mostrar_balao = True
                            config.indice_dialogo = 0
                        else:
                            config.indice_dialogo += 1
                            if config.indice_dialogo >= len(config.dialogo_npc1):
                                config.mostrar_balao = False

    # =========================================================================
    # ESTADO 4: A TRAVA DO PAUSE
    # =========================================================================
    if jogo_pausado:
        render.desenhar_pause(superficie_virtual, pause_selecionado, mostrar_controles_pause)
        
        proporcao_janela = largura_janela_real / altura_janela_real
        proporcao_virtual = LARGURA_VIRTUAL / ALTURA_VIRTUAL

        tela_redimensionada = pygame.transform.scale(superficie_virtual, (largura_janela_real, altura_janela_real))
        tela_real.fill((0, 0, 0))
        tela_real.blit(tela_redimensionada, (0, 0))

        pygame.display.flip()
        continue

    # =========================================================================
    # LÓGICA DE GAMEPLAY E FÍSICA (SÓ RODA SE NÃO ESTIVER PAUSADO)
    # =========================================================================
    area_conversa = rect_npc1.inflate(100, 50)
    if jogador.rect.colliderect(area_conversa):
        config.perto_do_npc = True
    else:
        config.perto_do_npc = False
        config.mostrar_balao = False

    jogador.gerenciar_movimento(teclas)
    jogador.aplicar_gravidade_e_colisao()
    jogador.atualizar_tiro(teclas, tempo_atual)
    jogador.atualizar_estados()
    sprite_jogador_atual = jogador.atualizar_animacao()

    for tiro in config.projeteis[:]:
        tiro.atualizar()
        if (tiro.rect.x > 1920 or tiro.rect.x < 0) and tiro in config.projeteis:
            config.projeteis.remove(tiro)

    for pinguim_atual in config.inimigos_cenario[:]:
        if pinguim_atual.vivo:
            pinguim_atual.atualizar_ia(jogador.rect)
            if jogador.rect.colliderect(pinguim_atual.rect):
                if config.tempo_escudo_restante <= 0:
                    if jogador.receber_dano(pinguim_atual):
                        config.game_over = True
            for tiro in config.projeteis[:]:
                if tiro.rect.colliderect(pinguim_atual.rect):
                    if tiro in config.projeteis:
                        config.projeteis.remove(tiro)
                    pinguim_atual.vida -= 1
                    if pinguim_atual.vida <= 0:
                        pinguim_atual.vivo = False
                        config.score += 100
                        config.tempo_descanso_inimigo = 0
                        if random.random() <= 0.6:
                            tipo_sorteado = random.choice(['vida', 'energia', 'escudo'])
                            novo_item = ItemColetavel(tipo_sorteado, pinguim_atual.rect.centerx, pinguim_atual.rect.centery)
                            config.itens_no_chao.append(novo_item)
                        if pinguim_atual in config.inimigos_cenario:
                            config.inimigos_cenario.remove(pinguim_atual)
                        if len(config.inimigos_cenario) == 0 and not config.crachas_gerados_na_fase and config.fase_atual > 0:
                            config.fases[config.fase_atual].spawnar_crachas(img_cracha)
                            config.crachas_gerados_na_fase = True
                        break

    if jogador.rect.x > 1920 or jogador.rect.x < 0:
        pode_avancar = (jogador.rect.x > 1920) and ((config.fase_atual + 1) in config.fases)
        pode_voltar = (jogador.rect.x < 0) and ((config.fase_atual - 1) in config.fases)

        if pode_avancar:
            config.fase_atual += 1
            config.carregar_fase(config.fase_atual)
            config.projeteis.clear()
            config.itens_no_chao.clear()
            jogador.rect.x = 10
        elif pode_voltar:
            config.fase_atual -= 1
            config.carregar_fase(config.fase_atual)
            config.projeteis.clear()
            config.itens_no_chao.clear()
            jogador.rect.x = 1910
        else:
            if jogador.rect.x > 1920:
                jogador.rect.right = 1920
            elif jogador.rect.x < 0:
                jogador.rect.x = 0

    if recursos.sprites_status_face:
        config.frame_rosto += config.velocidade_anim_rosto
        if config.frame_rosto >= len(recursos.sprites_status_face):
            config.frame_rosto = 0.0

    config.contador_frames_tempo += 1
    if config.contador_frames_tempo >= 60:
        config.tempo_segundos += 1
        config.contador_frames_tempo = 0

    # =========================================================================
    # DESENHO DA TELA E ITENS (O QUE ESTAVA FALTANDO!)
    # =========================================================================
    render.desenhar_tudo(superficie_virtual, jogador, fonte, rect_npc1, sprite_jogador_atual, img_cracha_hud)

    deslocamento_y = math.sin(tempo_atual * 0.005) * 8

    for item in config.itens_no_chao[:]:
        if isinstance(item, ItemColetavel):
            rect_flutuante = item.rect.copy()
            rect_flutuante.y += int(deslocamento_y)
            superficie_virtual.blit(item.image, rect_flutuante)
            if jogador.rect.colliderect(item.rect):
                config.inventario[item.tipo] += 1
                config.itens_no_chao.remove(item)
        else:
            rect_flutuante = item["rect"].copy()
            rect_flutuante.y += int(deslocamento_y)
            superficie_virtual.blit(item["imagem"], rect_flutuante)
            if jogador.rect.colliderect(item["rect"]):
                config.inventario["cracha"] += 1
                config.itens_no_chao.remove(item)

    proporcao_janela = largura_janela_real / altura_janela_real
    proporcao_virtual = LARGURA_VIRTUAL / ALTURA_VIRTUAL

    if proporcao_janela > proporcao_virtual:
        nova_altura = altura_janela_real
        nova_largura = int(nova_altura * proporcao_virtual)
    else:
        nova_largura = largura_janela_real
        nova_altura = int(nova_largura / proporcao_virtual)

    pos_x = (largura_janela_real - nova_largura) // 2
    pos_y = (altura_janela_real - nova_altura) // 2

    tela_redimensionada = pygame.transform.scale(superficie_virtual, (largura_janela_real, altura_janela_real))
    tela_real.fill((0, 0, 0))
    tela_real.blit(tela_redimensionada, (0, 0))

    
    pygame.display.flip()

pygame.quit()