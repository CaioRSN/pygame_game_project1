import pygame
import recursos
import config
import render  
from jogador import Jogador 
from inimigo import Inimigo

pygame.init()

tela = pygame.display.set_mode(config.tamanho_tela)
pygame.display.set_caption("Cin aventure")
largura_calculada = recursos.inicializar_recursos(config.tamanho_tela, config.ALTURA_PERSONAGEM)

jogador = Jogador(largura_calculada)
pinguim = Inimigo()


rect_npc1 = pygame.Rect(450, config.chao.y - 128, 64, 64)


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
    
    pinguim.vivo = True
    pinguim.vida = 3
    pinguim.rect.x = 1500

while config.rodando:
    clock.tick(60)
    tempo_atual = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed() 

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
        # Inputs globais de clique único
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                config.rodando = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and not jogador.pulando and not jogador.em_hit:
                    jogador.velocidade_y = -config.velocidade_pulo
                    jogador.pulando = True

            if evento.type == pygame.KEYDOWN:
             if evento.key == pygame.K_t:
            # Se o jogador estiver perto do NPC ao apertar T
               if config.perto_do_npc and config.indice_fundo == 0:
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

#"área de conversa" ao redor do NPC aumentando o tamanho do retângulo dele
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

        # Atualização dos Projéteis
        for tiro in config.projeteis[:]:
            fora_da_tela = tiro.atualizar()
            
            if pinguim.vivo and tiro.rect.colliderect(pinguim.rect):
                config.projeteis.remove(tiro) 
                pinguim.vida -= 1
                if pinguim.vida <= 0:
                    pinguim.vivo = False  
                    config.score += 100

                config.tempo_descanso_inimigo = 0
                continue 
                
            if fora_da_tela:
                 config.projeteis.remove(tiro)

        # Atualização do Inimigo
        if pinguim.vivo: 
            pinguim.atualizar_ia(jogador.rect) 
            sprite_inimigo_atual = pinguim.sprite_atual 
            
            # Gerencia colisão de dano no jogador
            if jogador.receber_dano(pinguim):
                config.game_over = True
        else:
            sprite_inimigo_atual = None 

  
        # Transição de Cenários
        if jogador.rect.x > 1920:
            if (config.fase_atual + 1) in config.fases:
                config.carregar_fase(config.fase_atual + 1) 
                config.projeteis.clear()  
                jogador.rect.x = 10  
            else:
                jogador.rect.right = 1920  
                
        elif jogador.rect.x < 0:
            if (config.fase_atual - 1) in config.fases:
                config.carregar_fase(config.fase_atual - 1) 
                config.projeteis.clear()  
                jogador.rect.x = 1910 - jogador.rect.width  
            else:
                jogador.rect.x = 0

        # Animação da HUD
        if recursos.sprites_status_face:
            config.frame_rosto += config.velocidade_anim_rosto
            if config.frame_rosto >= len(recursos.sprites_status_face):
                config.frame_rosto = 0.0

        # Relógio
        config.contador_frames_tempo += 1
        if config.contador_frames_tempo >= 60:  
            config.tempo_segundos += 1
            config.contador_frames_tempo = 0

        render.desenhar_tudo(tela, jogador, pinguim, sprite_inimigo_atual, sprite_mostrar, fonte, rect_npc1)

pygame.quit()