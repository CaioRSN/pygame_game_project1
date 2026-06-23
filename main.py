import pygame
import recursos
import config
import render  
import sys 

from jogador import Jogador 
from inimigo import Inimigo

pygame.init()

tela = pygame.display.set_mode(config.tamanho_tela)
<<<<<<< HEAD
pygame.display.set_caption("Cin Adventure")
=======
pygame.display.set_caption("Cin aventure")
>>>>>>> a01b04bf399d562fdd5dd3a52179b349f67d6e35
largura_calculada = recursos.inicializar_recursos(config.tamanho_tela, config.ALTURA_PERSONAGEM)

jogador = Jogador(largura_calculada)
rect_npc1 = pygame.Rect(450, config.chao.y - 128, 64, 64)

# Carrega a fase inicial configurando os cenários
pinguim = Inimigo()

if recursos.sprites_pinguin_parado:
    config.inimigo_rect.width = recursos.sprites_pinguin_parado[0].get_width()

config.ultimo_tempo = pygame.time.get_ticks()
clock = pygame.time.Clock()
sprite_inimigo_atual = None
fonte = pygame.font.SysFont("Arial", 20) 

config.tempo_descanso_inimigo = 0
config.game_over = False

config.carregar_fase(0)

def reiniciar_jogo():
    jogador.vida_atual = jogador.vida_maxima
    jogador.em_hit = False
    jogador.invulneravel = 0
    config.game_over = False
    config.tempo_descanso_inimigo = 0
    config.projeteis.clear()
    
    jogador.rect.x = config.POS_X_INICIAL
    jogador.rect.y = config.POS_Y_INICIAL
    jogador.velocidade_y = 0
    
    # Recarrega a fase atual do zero limpando os estados antigos dos inimigos
    config.carregar_fase(config.fase_atual)


#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------


while config.rodando:
    
    clock.tick(60)
    tempo_atual = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed() 

<<<<<<< HEAD
    if config.no_menu:
=======
    if no_menu:
>>>>>>> a01b04bf399d562fdd5dd3a52179b349f67d6e35
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
                
            if evento.type == pygame.KEYDOWN:
                if mostrar_controles:
                    if evento.key == pygame.K_ESCAPE:
                        mostrar_controles = False
                else:
                    if evento.key in (pygame.K_DOWN, pygame.K_s):
                        menu_selecionado = (menu_selecionado + 1) % 3
                    elif evento.key in (pygame.K_UP, pygame.K_w):
                        menu_selecionado = (menu_selecionado - 1) % 3
                    elif evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                        if menu_selecionado == 0:
                            no_menu = False 
                        elif menu_selecionado == 1:
                            mostrar_controles = True
                        elif menu_selecionado == 2:
                            config.rodando = False
                            pygame.quit()
                            sys.exit() 

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
        
        tela.blit(recursos.sprite_tela_game_over, (0, 0))
        cor_do_texto = (240, 240, 220) 
        texto_instrucao = recursos.fonte_game_over.render("PRESSIONE ESPACO PARA TENTAR NOVAMENTE", True, cor_do_texto)
        tela.blit(texto_instrucao, (565, 780))
        pygame.display.flip()
        continue

    else:

        # Inputs globais
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not jogador.pulando and not jogador.em_hit:
                    jogador.velocidade_y = -config.velocidade_pulo
                    jogador.pulando = True

                if evento.key == pygame.K_t:
                    # Se o jogador estiver perto do NPC ao apertar T
                    if config.perto_do_npc and config.fase_atual == 0:
                        if not config.mostrar_balao:
                            # Se o balão estava fechado, abre ele na primeira frase
                            config.mostrar_balao = True
                            config.indice_dialogo = 0
                        else:
                            # Se o balão já estava aberto, avança para a próxima frase
                            config.indice_dialogo += 1
                            # Se as frases acabaram, fecha o balão
                            if config.indice_dialogo >= len(config.dialogo_npc1):
                                config.mostrar_balao = False

        # LÓGICA DE PROXIMIDADE (Roda a cada frame no loop principal)
        # "área de conversa" ao redor do NPC aumentando o tamanho do retângulo dele
        area_conversa = rect_npc1.inflate(100, 50) # Aumenta 100px pros lados e 50px pra cima/baixo

        if jogador.rect.colliderect(area_conversa):
            config.perto_do_npc = True
        else:
            # Se o jogador se afastar do NPC, o balão some automaticamente
            config.perto_do_npc = False
            config.mostrar_balao = False

        # Atualização do Jogador (Movimento, Física, Tiro e Animação)
        jogador.gerenciar_movimento(teclas)
        jogador.aplicar_gravidade_e_colisao()
        jogador.atualizar_tiro(teclas, tempo_atual)
        jogador.atualizar_estados()
        sprite_mostrar = jogador.atualizar_animacao()

        # ATUALIZAÇÃO E COLISÃO DOS INIMIGOS
        for pinguim_atual in config.inimigos_cenario:
            if pinguim_atual.vivo:

                pinguim_atual.atualizar_ia(jogador.rect)
                
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

        # Atualização da posição das balas (movimento e limite de tela)
        for tiro in config.projeteis[:]:
            fora_da_tela = tiro.atualizar()
            if fora_da_tela and tiro in config.projeteis:
                config.projeteis.remove(tiro)

        # Transição de Cenários
        if jogador.rect.x > 1920 or jogador.rect.x < 0:
            # Salva quais pinguins morreram na fase que o jogador está SAINDO
            if config.fase_atual <= 4: # NUMERO DE FASES MAXIMAS

                config.inimigos_derrotados[config.fase_atual] = [
                    i for i, p in enumerate(config.inimigos_cenario) if not p.vivo
                ]

            # Define a nova fase desejada
            nova_fase = config.fase_atual + 1 if jogador.rect.x > 1920 else config.fase_atual - 1

            if nova_fase in config.fases:
                config.carregar_fase(nova_fase)
                config.projeteis.clear()
                
                if jogador.rect.x > 1920:
                    jogador.rect.x = 10
                else:
                    jogador.rect.x = 1910 - jogador.rect.width

                # Aplica o histórico de mortes na fase que o jogador acabou de ENTRAR
                if nova_fase in config.inimigos_derrotados:
                    indices_mortos = config.inimigos_derrotados[nova_fase]
                    for indice in indices_mortos:
                        if indice < len(config.inimigos_cenario):
                            config.inimigos_cenario[indice].vivo = False
                            config.inimigos_cenario[indice].vida = 0
            else:
                # Impede o jogador de sair dos limites se não houver próxima fase
                if jogador.rect.x > 1920:
                    jogador.rect.right = 1920
                else:
                    jogador.rect.x = 0

        # Atualização do Inimigo Individual (Pinguim do teste)
        if pinguim.vivo: 
            pinguim.atualizar_ia(jogador.rect) 
            sprite_inimigo_atual = pinguim.sprite_atual 
            
            # Gerencia colisão de dano no jogador
            if jogador.receber_dano(pinguim):
                config.game_over = True
            
            # Colisão dos projéteis com o pinguim de teste
            for tiro in config.projeteis[:]:
                if tiro.rect.colliderect(pinguim.rect):
                    if tiro in config.projeteis:
                        config.projeteis.remove(tiro) 
                    pinguim.vida -= 1
                    if pinguim.vida <= 0:
                        pinguim.vivo = False  
                        config.score += 100
                    config.tempo_descanso_inimigo = 0
        else:
            sprite_inimigo_atual = None 

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

        # Desenha tudo completo 
<<<<<<< HEAD
        render.desenhar_tudo(tela, jogador, fonte, rect_npc1, sprite_mostrar)
=======
        render.desenhar_tudo(tela, jogador, pinguim, sprite_inimigo_atual, sprite_mostrar, fonte, rect_npc1)
>>>>>>> a01b04bf399d562fdd5dd3a52179b349f67d6e35

pygame.quit()
