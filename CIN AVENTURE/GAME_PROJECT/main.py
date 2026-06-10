import pygame
import recursos
import config
import render  


#marcao é muito legal
pygame.init()

config.game_over = False

# Inicializa a janela e os recursos visuais
tela = pygame.display.set_mode(config.tamanho_tela)
pygame.display.set_caption("Cin aventure")
largura_calculada = recursos.inicializar_recursos(config.tamanho_tela, config.ALTURA_PERSONAGEM)

# Cria o retângulo do jogador e prepara o tempo e sprite iniciais
jogador = pygame.Rect(config.POS_X_INICIAL, config.POS_Y_INICIAL, largura_calculada, config.ALTURA_PERSONAGEM)

# Ajusta a largura do retângulo do inimigo baseado na imagem real carregada
if recursos.sprites_pinguin_parado:
    config.inimigo_rect.width = recursos.sprites_pinguin_parado[0].get_width()

config.ultimo_tempo = pygame.time.get_ticks()
personagem_sprite = recursos.sprite_personagem_scaled
clock = pygame.time.Clock()

sprite_inimigo_atual = None
fonte = pygame.font.SysFont("Arial", 20) 

# Controles do estado de Hit do Jogador 
config.jogador_em_hit = False
config.tempo_hit_jogador = 0
config.direcao_hit_jogador = 0
config.invulneravel_jogador = 0
config.tempo_descanso_inimigo = 0

config.vida_maxima = 5  # Quantidade total de corações na tela
config.vida_jogador = 5  # Quantidade de vida que ele começa

def reiniciar_jogo():
    config.vida_jogador = config.vida_maxima
    config.game_over = False
    config.jogador_em_hit = False
    config.invulneravel_jogador = 0
    config.tempo_descanso_inimigo = 0
    config.projeteis.clear()  # Limpa tiros que ficaram na tela
    
    # Reseta posições dos personagens
    jogador.x = config.POS_X_INICIAL
    jogador.y = config.POS_Y_INICIAL
    config.velocidade_y = 0
    
    config.inimigo_rect.x = 1500

# ----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------------------


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
                    reiniciar_jogo()  # Reseta tudo se apertar espaço
        
        
        # 'recursos.sprite_game_over'
        tela.blit(recursos.sprite_tela_game_over, (0, 0))

        cor_do_texto = (240, 240, 220) 
        texto_instrucao = recursos.fonte_game_over.render("PRESSIONE ESPACO PARA TENTAR NOVAMENTE", True, cor_do_texto)
        texto_x = 565  
        texto_y = 780  
        tela.blit(texto_instrucao, (texto_x, texto_y))
        
        pygame.display.flip()
        continue

        pygame.display.flip()
        continue  # Pula o resto do loop do jogo para nada se mover atrás da tela
        
  else:



     #Sistema de Vida

    # Eventos de fechar e pulo por clique único
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            config.rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not config.pulando and not config.jogador_em_hit:
                config.velocidade_y = -config.velocidade_pulo
                config.pulando = True

    # Lógica de disparo (Segurando K) - Só atira se não estiver tomando hit
    if teclas[pygame.K_k] and not config.jogador_em_hit:
        config.atacando = True  
        if tempo_atual - config.ultimo_disparo > config.cooldown_disparo:
            pos_x = jogador.right if config.direcao == "direita" else jogador.left - 30
            pos_y_ajustado = jogador.centery - 30 

            novo_tiro = {
                "rect": pygame.Rect(pos_x, pos_y_ajustado, 30, 30),
                "tipo_sprite": config.indice_sprite_projetil,
                "direcao": 1 if config.direcao == "direita" else -1
            }
            
            config.projeteis.append(novo_tiro)
            config.indice_sprite_projetil = 1 - config.indice_sprite_projetil
            config.ultimo_disparo = tempo_atual
    else:
        config.atacando = False  

    if True:
        # Atualizar movimentação dos projéteis pela tela
        for tiro in config.projeteis[:]:
            tiro["rect"].x += 10 * tiro["direcao"] 
            if tiro["rect"].x < 0 or tiro["rect"].x > 1920:
                 config.projeteis.remove(tiro)
                 continue  

            # Teste de colisão com o Pinguim (Inimigo apenas reseta de posição ao morrer por enquanto)
            if config.inimigo_vivo and tiro["rect"].colliderect(config.inimigo_rect):
                config.vida_inimigo -= 1  
                config.projeteis.remove(tiro)
                
                if config.vida_inimigo <= 0:
                    config.vida_inimigo = 3             
                    config.inimigo_rect.x = 1500         

        # Movimentação do Jogador (Bloqueada se estiver em estado de Hit)
        movendo = False 
        if not config.atacando and not config.jogador_em_hit:
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                jogador.x -= config.velocidade_jogador
                config.direcao = "esquerda"
                movendo = True
            
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                jogador.x += config.velocidade_jogador
                config.direcao = "direita"
                movendo = True

            if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and not config.pulando:
                config.velocidade_y = -config.velocidade_pulo
                config.pulando = True

        # Aplica gravidade contínua
        config.velocidade_y += config.gravidade
        jogador.y += config.velocidade_y
    
        # Colisão física com o Chão fixo
        if jogador.colliderect(config.chao) and config.velocidade_y >= 0:
            jogador.bottom = config.chao.top
            config.velocidade_y = 0
            config.pulando = False

        # --- Colisão física com as Plataformas e Blocos ---
        for lista_plat in config.plataformas_flutuantes:
            rect_colisao = lista_plat[0]
            if jogador.colliderect(rect_colisao) and config.velocidade_y >= 0:
                if jogador.bottom <= rect_colisao.top + config.velocidade_y + 1:
                    jogador.bottom = rect_colisao.top
                    config.velocidade_y = 0
                    config.pulando = False

        for lista_bloco in config.blocos_cenario:
            rect_colisao = lista_bloco[0]
            if jogador.colliderect(rect_colisao) and config.velocidade_y >= 0:
                if jogador.bottom <= rect_colisao.top + config.velocidade_y + 1:
                    jogador.bottom = rect_colisao.top
                    config.velocidade_y = 0
                    config.pulando = False
        
        # --- Transição de Cenários pelas Bordas da Tela ---
        if jogador.x > 1920:
            if (config.fase_atual + 1) in config.fases:
                config.carregar_fase(config.fase_atual + 1)
                jogador.x = 10  
            else:
                jogador.right = 1920  

        elif jogador.x < 0:
            if (config.fase_atual - 1) in config.fases:
                config.carregar_fase(config.fase_atual - 1)
                jogador.x = 1910 - jogador.width  
            else:
                jogador.x = 0  


        # --- Controle e Movimentação do Inimigo ---
        inimigo_movendo = False
        inimigo_atacando = False

        if config.inimigo_vivo:

           if config.tempo_descanso_inimigo > 0:
                config.tempo_descanso_inimigo -= 1
                # Força ele a ficar no estado parado
                distancia_x = 9999 
                distancia_y = 9999
           else:

            # Calcula as distâncias em ambos os eixos
            distancia_x = abs(jogador.x - config.inimigo_rect.x)
            distancia_y = abs(jogador.y - config.inimigo_rect.y)
            
            estado_anterior_pinguim = "parado"
            if sprite_inimigo_atual in recursos.sprites_pinguin_andando:
                estado_anterior_pinguim = "andando"
            elif sprite_inimigo_atual in recursos.sprites_pinguin_atacando:
                estado_anterior_pinguim = "atacando"

            # 1. Definição do comportamento da Inteligência Artificial
            if distancia_x < 80 and distancia_y < 50:
                inimigo_atacando = True
            elif distancia_x < 500 and distancia_y < 150:
                # Perseguição com zona morta de 15px para evitar tremer embaixo de plataformas
                if (jogador.x - config.inimigo_rect.x) > 15:
                    config.inimigo_rect.x += config.velocidade_inimigo
                    config.direcao_inimigo = "direita"
                    inimigo_movendo = True
                elif (jogador.x - config.inimigo_rect.x) < -15:
                    config.inimigo_rect.x -= config.velocidade_inimigo
                    config.direcao_inimigo = "esquerda"
                    inimigo_movendo = True
                else:
                    inimigo_movendo = False

            # 2. Seleção de animação do Pinguim
            if inimigo_atacando:
                estado_novo_pinguim = "atacando"
                lista_animacao_pinguim = recursos.sprites_pinguin_atacando
                velocidade_anim_pinguim = 0.15
            elif inimigo_movendo:
                estado_novo_pinguim = "andando"
                lista_animacao_pinguim = recursos.sprites_pinguin_andando
                velocidade_anim_pinguim = 0.12
            else:
                estado_novo_pinguim = "parado"
                lista_animacao_pinguim = recursos.sprites_pinguin_parado
                velocidade_anim_pinguim = 0.05

            if estado_novo_pinguim != estado_anterior_pinguim:
                config.frame_inimigo = 0.0

            # 3. Processamento de frames do Pinguim
            if lista_animacao_pinguim:
                config.frame_inimigo += velocidade_anim_pinguim
                if config.frame_inimigo >= len(lista_animacao_pinguim):
                    config.frame_inimigo = 0
                sprite_inimigo_atual = lista_animacao_pinguim[int(config.frame_inimigo)]
        else:
            sprite_inimigo_atual = None


         # COLISÃO DO ATAQUE DO PINCOIM NO JOGADOR 
        if config.inimigo_vivo and inimigo_atacando:
            if jogador.colliderect(config.inimigo_rect) and not config.jogador_em_hit and config.invulneravel_jogador <= 0:
                config.jogador_em_hit = True
                
                
                config.tempo_hit_jogador = 48  
                
                config.invulneravel_jogador = 75 
                config.frame_atual = 0.0       
                config.tempo_descanso_inimigo = 60
                
                config.vida_jogador -= 1
                if config.vida_jogador < 1:
                    config.vida_jogador = 0 #garante que nn fica negativo 
                    config.game_over = True

                if config.inimigo_rect.x < jogador.x:
                    config.direcao_hit_jogador = 1  
                else:
                    config.direcao_hit_jogador = -1


        # --- Máquina de Estados da Animação do Jogador

        if config.jogador_em_hit:
            var_lista_atual = recursos.sprites_personagem_pos_hit
            
            velocidade_anim_atual = 0.13
            
            if config.tempo_hit_jogador > 28:
                jogador.x += 7 * config.direcao_hit_jogador # Empurrão forte e rápido no início
            
            config.tempo_hit_jogador -= 1
            if config.tempo_hit_jogador <= 0:
                config.jogador_em_hit = False


        elif config.atacando:
            var_lista_atual = recursos.sprites_atacando
            velocidade_anim_atual = 0.15 
            
        elif config.pulando:
            config.frame_atual = 0 
            if config.velocidade_y < -5:
                personagem_sprite = recursos.sprite_prepara_pulo
            elif -5 <= config.velocidade_y <= 5:
                personagem_sprite = recursos.sprite_no_ar
            else:
                personagem_sprite = recursos.sprite_caindo
        else:
            if movendo:
                var_lista_atual = recursos.sprites_correndo
                velocidade_anim_atual = 0.25 
            else:
                var_lista_atual = recursos.sprites_parado
                velocidade_anim_atual = 0.02

        # Atualização universal de animações baseadas em listas para o jogador
        if not config.pulando or config.jogador_em_hit:
            config.frame_atual += velocidade_anim_atual
            if config.frame_atual >= len(var_lista_atual):
                config.frame_atual = 0
            personagem_sprite = var_lista_atual[int(config.frame_atual)]

        # Diminui a invulnerabilidade do jogador a cada frame do jogo
        if config.invulneravel_jogador > 0:
            config.invulneravel_jogador -= 1

        # Animação do Rosto de Status
        if recursos.sprites_status_face:
            config.frame_rosto += config.velocidade_anim_rosto
            if config.frame_rosto >= len(recursos.sprites_status_face):
                config.frame_rosto = 0.0

        # Inversão de direção do sprite do jogador
        if config.direcao == "esquerda":
            sprite_mostrar = pygame.transform.flip(personagem_sprite, True, False)  
        else:
            sprite_mostrar = personagem_sprite  
        

        # Sistema do Relógio / Tempo do cenário
        config.contador_frames_tempo += 1
        if config.contador_frames_tempo >= 60:  
            config.tempo_segundos += 1
            config.contador_frames_tempo = 0

        # Chamada unificada para desenhar a interface e elementos
        render.desenhar_tudo(tela, jogador, sprite_inimigo_atual, sprite_mostrar, fonte)

pygame.quit()
