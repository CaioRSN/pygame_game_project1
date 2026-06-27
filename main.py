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
        self.tipo = tipo  # 'vida', 'energia' ou 'escudo'
        if tipo == 'vida':
            self.image = recursos.item_vida_img
        elif tipo == 'energia':
            self.image = recursos.item_energia_img
        elif tipo == 'escudo':
            self.image = recursos.item_escudo_img
        self.rect = self.image.get_rect(center=(x, y))

pygame.init()
tela = pygame.display.set_mode(config.tamanho_tela)
pygame.display.set_caption("Cin Adventure")

largura_calculada = recursos.inicializar_recursos(config.tamanho_tela, config.ALTURA_PERSONAGEM)
jogador = Jogador(largura_calculada)

# Posicionamento corrigido do NPC
rect_npc1 = pygame.Rect(450, config.chao.y - 128, 64, 64)

config.ultimo_tempo = pygame.time.get_ticks()
clock = pygame.time.Clock()
fonte = pygame.font.SysFont("Arial", 20)

config.tempo_descanso_inimigo = 0
config.game_over = False

# Inicializa variáveis extras de controle de itens caso não existam no config
if not hasattr(config, 'velocidade_aumentada'):
    config.velocidade_aumentada = False
if not hasattr(config, 'tempo_escudo_restante'):
    config.tempo_escudo_restante = 0
if not hasattr(config, 'tempo_energia_restante'):
    config.tempo_energia_restante = 0

config.carregar_fase(0)

if not hasattr(config, 'itens_no_chao'):
    config.itens_no_chao = []
if not hasattr(config, 'inventario'):
    config.inventario = {"vida": 0, "energia": 0, "escudo": 0}

def reiniciar_jogo():
    jogador.vida_atual = jogador.vida_maxima
    jogador.em_hit = False
    jogador.invulneravel = 0
    config.game_over = False
    config.tempo_descanso_inimigo = 0
    config.velocidade_aumentada = False
    config.tempo_escudo_restante = 0
    config.tempo_energia_restante = 0
    jogador.velocidade = 8  # Velocidade padrão inicial
    config.projeteis.clear()
    config.itens_no_chao.clear()
    jogador.rect.x = config.POS_X_INITIAL
    jogador.rect.y = config.POS_Y_INITIAL
    jogador.velocidade_y = 0
    config.carregar_fase(config.fase_atual)

menu_selecionado = 0
mostrar_controles = False

while config.rodando:
    clock.tick(60)
    tempo_atual = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed()
    config.plataformas = config.fases[config.fase_atual].atualizar_plataformas(jogador.rect, jogador.pulando)
    # --- LÓGICA DE TEMPO DOS ITENS ATIVOS ---
    if config.tempo_escudo_restante > 0:
        config.tempo_escudo_restante -= 1
        
    if config.tempo_energia_restante > 0:
        config.tempo_energia_restante -= 1
        config.velocidade_aumentada = True
        jogador.velocidade = 13  # Mantém a velocidade alta ativa durante os frames
        if config.tempo_energia_restante == 0:
            config.velocidade_aumentada = False
            jogador.velocidade = 8  # Retorna à velocidade padrão
    
    # --- LOGICA DE MENU
    if config.no_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrar_controles = False
                elif evento.key == pygame.K_SPACE:
                    if mostrar_controles:
                        mostrar_controles = False
                if not mostrar_controles:
                    if evento.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selecionado = (menu_selecionado + 1) % 3
                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        menu_selecionado = (menu_selecionado - 1) % 3
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                        if menu_selecionado == 0:
                            config.no_menu = False
                        elif menu_selecionado == 1:
                            mostrar_controles = True
                        elif menu_selecionado == 2:
                            config.rodando = False
                            
        render.desenhar_menu(tela, menu_selecionado, mostrar_controles)
        pygame.display.flip()
        continue
        
    # LÓGICA DE GAME OVER
    if config.game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_jogo()
                    
        tela.blit(recursos.sprite_tela_game_over, (0, 0))
        cor_do_texto = (240, 240, 220)
        texto_instrucao = recursos.fonte_game_over.render("PRESSIONE ESPACO PARA TENTAR NOVAMENTE", True, cor_do_texto)
        tela.blit(texto_instrucao, (565, 780))
        pygame.display.flip()
        continue
        
    # --- JOGO ATIVO
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            config.rodando = False
            
        # LÓGICA DE USO DOS ITENS PELO CLIQUE DO MOUSE (ORDEM DA HUD: VIDA, ENERGIA, ESCUDO)
        if evento.type == pygame.MOUSEBUTTONDOWN:
            if evento.button == 1:  # Botão esquerdo do mouse
                mx, my = pygame.mouse.get_pos()
                
                posicoes_x = [195, 260, 325]
                y_pos = 95
                largura_slot = 50
                altura_slot = 50
                
                # 1. Clique em VIDA (Slot 1)
                if posicoes_x[0] <= mx <= posicoes_x[0] + largura_slot and y_pos <= my <= y_pos + altura_slot:
                    if config.inventario["vida"] > 0:
                        if jogador.vida_atual < jogador.vida_maxima:
                            config.inventario["vida"] -= 1
                            jogador.vida_atual += 1
                        
                # 2. Clique em ENERGIA (Slot 2)
                elif posicoes_x[1] <= mx <= posicoes_x[1] + largura_slot and y_pos <= my <= y_pos + altura_slot:
                    if config.inventario["energia"] > 0:
                        config.inventario["energia"] -= 1
                        config.tempo_energia_restante = 600  # 10 segundos ativos
                        jogador.velocidade = 13
                            
                # 3. Clique em ESCUDO (Slot 3)
                elif posicoes_x[2] <= mx <= posicoes_x[2] + largura_slot and y_pos <= my <= y_pos + altura_slot:
                    if config.inventario["escudo"] > 0:
                        config.inventario["escudo"] -= 1
                        config.tempo_escudo_restante = 600  # Protegido por 10 segundos
                        
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not jogador.pulando and not jogador.em_hit:
                jogador.velocidade_y = -config.velocidade_pulo
                jogador.pulando = True
                
            if evento.key == pygame.K_t:
                if config.perto_do_npc and config.fase_atual == 0:
                    if not config.mostrar_balao:
                        config.mostrar_balao = True
                        config.indice_dialogo = 0
                    else:
                        config.indice_dialogo += 1
                        if config.indice_dialogo >= len(recursos.dialogo_npc1):
                            config.mostrar_balao = False
                            
    # Lógica de Proximidade do NPC
    area_conversa = rect_npc1.inflate(100, 50)
    if jogador.rect.colliderect(area_conversa):
        config.perto_do_npc = True
    else:
        config.perto_do_npc = False
        config.mostrar_balao = False
        
    # Atualização do Jogador
    jogador.gerenciar_movimento(teclas)
    jogador.aplicar_gravidade_e_colisao()
    jogador.atualizar_tiro(teclas, tempo_atual)
    jogador.atualizar_estados()
    sprite_jogador_atual = jogador.atualizar_animacao()
    
    # PROJETEIS: MOVIMENTAÇÃO
    for tiro in config.projeteis[:]:
        fora_da_tela = tiro.atualizar()
        if fora_da_tela and tiro in config.projeteis:
            config.projeteis.remove(tiro)
            
    # ATUALIZAÇÃO E COLISÃO DOS INIMIGOS (CENÁRIO)
    for pinguim_atual in config.inimigos_cenario[:]:
        if pinguim_atual.vivo:
            pinguim_atual.atualizar_ia(jogador.rect)
            
            # Jogador só recebe dano se NÃO estiver protegido pelo efeito do Escudo
            if jogador.rect.colliderect(pinguim_atual.rect):
                if config.tempo_escudo_restante <= 0:
                    if jogador.receber_dano(pinguim_atual):
                        config.game_over = True
                        
            # Colisão dos tiros com este pinguim
            for tiro in config.projeteis[:]:
                if tiro.rect.colliderect(pinguim_atual.rect):
                    if tiro in config.projeteis:
                        config.projeteis.remove(tiro)
                    pinguim_atual.vida -= 1
                    if pinguim_atual.vida <= 0:
                        pinguim_atual.vivo = False
                        config.score += 100
                        config.tempo_descanso_inimigo = 0
                        
                        # Sorteia e joga o item no chão usando a posição do pinguim
                        if random.random() < 0.6:
                            tipo_sorteado = random.choice(['vida', 'energia', 'escudo'])
                            novo_item = ItemColetavel(tipo_sorteado, pinguim_atual.rect.centerx, pinguim_atual.rect.centery)
                            config.itens_no_chao.append(novo_item)
                            
                        if pinguim_atual in config.inimigos_cenario:
                            config.inimigos_cenario.remove(pinguim_atual)
                        break
                        
    # TRANSIÇÃO DE CENÁRIOS
    if jogador.rect.x > 1920 or jogador.rect.x < 0:
        if config.fase_atual <= 4:
            nova_fase = config.fase_atual + 1 if jogador.rect.x > 1920 else config.fase_atual - 1
            if nova_fase in config.fases:
                config.carregar_fase(nova_fase)
                config.projeteis.clear()
                config.itens_no_chao.clear()
                if jogador.rect.x > 1920:
                    jogador.rect.x = 10
                else:
                    jogador.rect.x = 1910
            else:
                if jogador.rect.x > 1920:
                    jogador.rect.right = 1920
                else:
                    jogador.rect.x = 0
                    
    # Animação da HUD
    if recursos.sprites_status_face:
        config.frame_rosto += config.velocidade_anim_rosto
        if config.frame_rosto >= len(recursos.sprites_status_face):
            config.frame_rosto = 0.0
            
    # Relógio do Jogo
    config.contador_frames_tempo += 1
    if config.contador_frames_tempo >= 60:
        config.tempo_segundos += 1
        config.contador_frames_tempo = 0
        
    # Desenha o cenário, personagens e a HUD de fundo primeiro[cite: 3]
    render.desenhar_tudo(tela, jogador, fonte, rect_npc1, sprite_jogador_atual)
    
    # Renderização e Coleta de Itens do Chão
    for item in config.itens_no_chao[:]:
        tela.blit(item.image, item.rect)
        if jogador.rect.colliderect(item.rect):
            config.inventario[item.tipo] += 1
            config.itens_no_chao.remove(item)
            
    pygame.display.flip()

pygame.quit()
