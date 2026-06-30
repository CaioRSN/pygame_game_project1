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

# --- CARREGAMENTO DA TELA INICIAL ---
try:
    img_tela_inicial = pygame.image.load("imagens_e_texturas/tela_inicial.png").convert()
    img_tela_inicial = pygame.transform.scale(img_tela_inicial, config.tamanho_tela)
except Exception as e:
    print("Erro ao carregar tela inicial:", e)
    img_tela_inicial = pygame.Surface(config.tamanho_tela)
    img_tela_inicial.fill((20, 20, 30))

na_tela_inicial = True

# Carrega a imagem do crachá para ser usada no spawn e HUD
try:
    img_cracha_original = pygame.image.load("objeto cracha.png").convert_alpha()
    img_cracha = pygame.transform.scale(img_cracha_original, (40, 40))
    img_cracha_hud = pygame.transform.scale(img_cracha_original, (35, 35))
except Exception as e:
    print(e)
    img_cracha = pygame.Surface((40, 40))
    img_cracha.fill((255, 215, 0))
    img_cracha_hud = pygame.transform.scale(img_cracha, (35, 35))

# Posicionamento corrigido do NPC
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

# função para reiniciar o jogo
def reiniciar_jogo():
    jogador.vida_atual = jogador.vida_maxima
    jogador.em_hit = False
    jogador.invulneravel = 0
    config.game_over = False
    config.tempo_descanso_inimigo = 0
    config.velocidade_aumentada = False
    config.tempo_escudo_restante = 0
    config.tempo_energia_restante = 0
    config.cooldown_tiro_reduzido = False
    jogador.velocidade = 5
    config.projeteis.clear()
    config.itens_no_chao.clear()
    jogador.rect.x = config.POS_X_INICIAL
    jogador.rect.y = config.POS_Y_INICIAL
    jogador.velocidade_y = 0
    config.carregar_fase(config.fase_atual)


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

menu_selecionado = 0
mostrar_controles = False

# --- AJUSTE DOS ESTADOS INICIAIS ---
na_tela_inicial = False
config.no_menu = True    # Garante que o menu com opções vai abrir depois

# LOOP EXCLUSIVO DA TELA INICIAL
while na_tela_inicial and config.rodando:
    clock.tick(60)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            config.rodando = False
            na_tela_inicial = False
        # Qualquer tecla ou clique faz avançar para o Menu Interativo
        if evento.type == pygame.KEYDOWN or evento.type == pygame.MOUSEBUTTONDOWN:
            na_tela_inicial = False

    tela.blit(img_tela_inicial, (0, 0))
    pygame.display.flip()

# --- LOOP PRINCIPAL DO JOGO ---
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

    if config.no_menu:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    mostrar_controles = False
                
                if mostrar_controles:
                    if evento.key == pygame.K_SPACE:
                        mostrar_controles = False
                else:
                    # Movimentação nas opções do menu
                    if evento.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selecionado = (menu_selecionado + 1) % 3
                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        menu_selecionado = (menu_selecionado - 1) % 3
                    # Confirmar a opção selecionada
                    elif evento.key in (pygame.K_RETURN, pygame.K_KP_ENTER, pygame.K_SPACE):
                        if menu_selecionado == 0:
                            config.no_menu = False  # Inicia o jogo
                        elif menu_selecionado == 1:
                            mostrar_controles = True # Abre os controles
                        elif menu_selecionado == 2:
                            config.rodando = False   # Sair do jogo
                            
        render.desenhar_menu(tela, menu_selecionado, mostrar_controles)
        pygame.display.flip()
        continue

    if config.game_over:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    reiniciar_jogo()
        tela.blit(recursos.sprite_tela_game_over, (0,0))
        cor_do_texto = (240,240,220)
        texto_instrucao = recursos.fonte_game_over.render("PRESSIONE ESPACO PARA TENTAR NOVAMENTE", True, cor_do_texto)
        tela.blit(texto_instrucao, (565, 780))
        pygame.display.flip()
        continue

    # inicia o loop pra detectar ações que fizer no jogo
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            config.rodando = False
                    
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not jogador.pulando and not jogador.em_hit:
                jogador.pulando = True
                jogador.velocidade_y = -config.velocidade_pulo
            if evento.key == pygame.K_UP and not jogador.pulando and not jogador.em_hit:
                jogador.pulando = True
                jogador.velocidade_y = -config.velocidade_pulo
                
            if evento.key == pygame.K_t:
                if config.perto_do_npc and config.fase_atual == 0:
                    if not config.mostrar_balao:
                        config.mostrar_balao = True
                        config.indice_dialogo = 0
                    else:
                        config.indice_dialogo += 1
                        if config.indice_dialogo >= len(config.dialogo_npc1):
                            config.mostrar_balao = False

            if evento.key == pygame.K_1:
                usar_vida()

            if evento.key == pygame.K_2:
                usar_energia()

            if evento.key == pygame.K_3:
                usar_escudo()

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
        if config.fase_atual <= 4:
            nova_fase = config.fase_atual + 1 if jogador.rect.x > 1920 else config.fase_atual
            if jogador.rect.x < 0 and config.fase_atual > 0:
                nova_fase = config.fase_atual - 1
                
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

    if recursos.sprites_status_face:
        config.frame_rosto += config.velocidade_anim_rosto
        if config.frame_rosto >= len(recursos.sprites_status_face):
            config.frame_rosto = 0.0

    config.contador_frames_tempo += 1
    if config.contador_frames_tempo >= 60:
        config.tempo_segundos += 1
        config.contador_frames_tempo = 0

    render.desenhar_tudo(tela, jogador, fonte, rect_npc1, sprite_jogador_atual)

    for item in config.itens_no_chao[:]:
        if isinstance(item, ItemColetavel):
            tela.blit(item.image, item.rect)
            if jogador.rect.colliderect(item.rect):
                config.inventario[item.tipo] += 1
                config.itens_no_chao.remove(item)
        else:
            tela.blit(item["imagem"], item["rect"])
            if jogador.rect.colliderect(item["rect"]):
                config.inventario["cracha"] += 1
                config.itens_no_chao.remove(item)

    tela.blit(img_cracha_hud, (1780, 30))
    texto_cracha = fonte_hud_cracha.render(f"x {config.inventario['cracha']}", True, (255, 255, 255))
    tela.blit(texto_cracha, (1825, 32))

    pygame.display.flip()

pygame.quit()
