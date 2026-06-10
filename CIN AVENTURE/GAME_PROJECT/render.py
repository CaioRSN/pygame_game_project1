import pygame
import config
import recursos

def desenhar_tudo(tela, jogador, sprite_inimigo_atual, sprite_mostrar, fonte):
    
    tela.blit(recursos.fundos[config.indice_fundo], (0, 0))

    # 2. Desenha os Sprites das Plataformas Flutuantes
    for lista_plat in config.plataformas_flutuantes:
        rect_colisao = lista_plat[0]
        indice_sprite = lista_plat[1]
        
        sprite_original = recursos.sprites_plataformas[indice_sprite]
        sprite_esticado = pygame.transform.scale(sprite_original, (rect_colisao.width, rect_colisao.height))
        tela.blit(sprite_esticado, (rect_colisao.x, rect_colisao.y))

    # 3. Desenha os Sprites dos Blocos de Cenário
    for lista_bloco in config.blocos_cenario:
        rect_colisao = lista_bloco[0]
        indice_sprite = lista_bloco[1]
        
        sprite_bloco = recursos.sprites_blocos[indice_sprite]
        tela.blit(sprite_bloco, (rect_colisao.x, rect_colisao.y))        

    #Desenha o HUD de Status (Rosto + Corações)
    if recursos.sprites_status_face and recursos.sprite_coracao and recursos.sprite_coracao_vazio:
        rosto_x = 60
        rosto_y = 35
        
        sprite_rosto_atual = recursos.sprites_status_face[int(config.frame_rosto)]
        tela.blit(sprite_rosto_atual, (rosto_x, rosto_y))
        
        pos_x_inicial_coracoes = rosto_x + 125
        pos_y_coracoes = rosto_y + 15  
        espacamento = 45

        
        for i in range(config.vida_maxima):
            x_atual = pos_x_inicial_coracoes + (i * espacamento)
            
            # Se o índice atual for menor que a vida que resta, desenha o cheio
            if i < config.vida_jogador:
                tela.blit(recursos.sprite_coracao, (x_atual, pos_y_coracoes))
            # Se o índice for igual ou maior, significa que o coração já "esvaziou"
            else:
                tela.blit(recursos.sprite_coracao_vazio, (x_atual, pos_y_coracoes))

    # 5. Desenha o HUD do Timer
    if recursos.fonte_pixel_titulo and recursos.fonte_pixel_numero:
        COR_VERMELHA = (235, 45, 45)    
        COR_BEGE = (240, 240, 220)      

        minutos = config.tempo_segundos // 60
        segundos = config.tempo_segundos % 60
        texto_relogio = f"{minutos:02d}:{segundos:02d}"
        
        hud_time_titulo = recursos.fonte_pixel_titulo.render("TIMER", True, COR_VERMELHA)
        hud_time_relogio = recursos.fonte_pixel_numero.render(texto_relogio, True, COR_BEGE)

        timer_x = 1640  
        timer_y = 70
        
        tela.blit(hud_time_titulo, (timer_x, timer_y))
        tela.blit(hud_time_relogio, (timer_x, timer_y + 40))

    # 6. Desenha as Entidades Dinâmicas (personagem, Inimigos e Tiros na frente de tudo)
    pos_x_centralizado = jogador.centerx - (sprite_mostrar.get_width() // 2)
    tela.blit(sprite_mostrar, (pos_x_centralizado, jogador.y))
    
    if recursos.sprites_pinguin_parado and sprite_inimigo_atual is not None and config.inimigo_vivo:
        if config.direcao_inimigo == "esquerda":
            sprite_inimigo_mostrar = pygame.transform.flip(sprite_inimigo_atual, True, False)
        else:
            sprite_inimigo_mostrar = sprite_inimigo_atual

        pos_x_inimigo_centralizado = config.inimigo_rect.centerx - (sprite_inimigo_mostrar.get_width() // 2)
        tela.blit(sprite_inimigo_mostrar, (pos_x_inimigo_centralizado, config.inimigo_rect.y))

    for tiro in config.projeteis:
        img_tiro = recursos.sprites_projeteis[tiro["tipo_sprite"]]
        if tiro["direcao"] == -1:
            img_tiro = pygame.transform.flip(img_tiro, True, False)
        tela.blit(img_tiro, (tiro["rect"].x, tiro["rect"].y))


    largura_bloco_chao = 100
    # Redimensiona o sprite para a altura do seu chão mantendo a proporção quadrada
    sprite_chao_ajustado = pygame.transform.scale(recursos.sprite_chao, (largura_bloco_chao, config.chao.height))

    for x_atual in range(0, config.tamanho_tela[0], largura_bloco_chao):
     tela.blit(sprite_chao_ajustado, (x_atual, config.chao.y))


    # Coordenadas do cursor para ajudar no desenvolvimento
    mx, my = pygame.mouse.get_pos()
    texto = fonte.render(f"X: {mx}, Y: {my}", True, (255, 255, 255))
    tela.blit(texto, (mx + 10, my - 20))

    # Atualiza a tela de fato
    pygame.display.flip()
