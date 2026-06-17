import pygame
import config
import recursos
import math

def desenhar_tudo(tela, jogador, pinguim, sprite_inimigo_atual, sprite_mostrar, fonte, rect_npc):
    
    tela.blit(recursos.fundos[config.indice_fundo], (0, 0))

    # Desenha as plataformas
    for lista_plat in config.plataformas_flutuantes:
        rect_colisao = lista_plat[0]
        indice_sprite = lista_plat[1]
        
        sprite_original = recursos.sprites_plataformas[indice_sprite]
        sprite_esticado = pygame.transform.scale(sprite_original, (rect_colisao.width, rect_colisao.height))
        tela.blit(sprite_esticado, (rect_colisao.x, rect_colisao.y))

    # Desenha os blocos
    for lista_bloco in config.blocos_cenario:
        rect_colisao = lista_bloco[0]
        indice_sprite = lista_bloco[1]
        
        sprite_bloco = recursos.sprites_blocos[indice_sprite]
        tela.blit(sprite_bloco, (rect_colisao.x, rect_colisao.y))        

    # HUD da vida
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
            
            if i < jogador.vida_atual:
                tela.blit(recursos.sprite_coracao, (x_atual, pos_y_coracoes))
            else:
                tela.blit(recursos.sprite_coracao_vazio, (x_atual, pos_y_coracoes))


     # HUD do Inventário (3 Blocos, Itens e Quantidades)
    if recursos.sprite_bloco_inventario and len(recursos.sprite_itens) >= 3:
        posicoes_x = [195, 260, 325]
        y_pos = 95
        chaves_itens = ["item_1", "item_2", "item_3"]
        COR_TEXTO = (255, 215, 0)
        COR_SOMBRA = (0, 0, 0)


    for i in range(3):
            x_atual = posicoes_x[i]
            
            # Desenha a caixinha do inventário
            tela.blit(recursos.sprite_bloco_inventario, (x_atual, y_pos))
            
            # Desenha o Item dentro da caixinha 
            sprite_item = recursos.sprite_itens[i]
            tela.blit(sprite_item, (x_atual + 10, y_pos + 10))
            
   
            qtd = config.inventario_quantidades[chaves_itens[i]]
            
      
            texto_sombra = recursos.fonte_hud_itens.render(f"{qtd}", True, COR_SOMBRA)
            texto_qtd = recursos.fonte_hud_itens.render(f"{qtd}", True, COR_TEXTO)
            
            # Posição onde o texto vai ficar
            txt_x = x_atual + 35
            txt_y = y_pos + 38
            
            #Desenha a sombra preta deslocada 2 pixels para o lado e para baixo
            tela.blit(texto_sombra, (txt_x + 2, txt_y + 2))
            
            #Desenha o seu texto amarelo por cima
            tela.blit(texto_qtd, (txt_x, txt_y))


    # HUD do Timer
    if recursos.fonte_pixel_titulo and recursos.fonte_pixel_numero:
       
        COR_SOMBRA = (0, 0, 0) #sombra

        minutos = config.tempo_segundos // 60
        segundos = config.tempo_segundos % 60
        texto_relogio = f"{minutos:02d}:{segundos:02d}"
        
        #Cria os textos normais e as suas respectivas sombras
        hud_time_titulo = recursos.fonte_pixel_titulo.render("TIMER", True, (255, 0, 0))
        sombra_titulo = recursos.fonte_pixel_titulo.render("TIMER", True, COR_SOMBRA)
        
        hud_time_relogio = recursos.fonte_pixel_numero.render(texto_relogio, True, (255, 215, 0))
        sombra_relogio = recursos.fonte_pixel_numero.render(texto_relogio, True, COR_SOMBRA)

        timer_x = 850
        timer_y = 40
        
        # Desenha a sombra do título "TIMER" (+2 pixels de deslocamento)
        tela.blit(sombra_titulo, (timer_x + 2, timer_y + 2))
        # Desenha o título original por cima
        tela.blit(hud_time_titulo, (timer_x, timer_y))

        # Desenha a sombra dos números do relógio (+2 pixels de deslocamento)
        tela.blit(sombra_relogio, (timer_x + 2, timer_y + 40 + 2))
        # Desenha o relógio original por cima
        tela.blit(hud_time_relogio, (timer_x, timer_y + 40))

    # HUD do Score (Pontuação)
    if recursos.fonte_pixel_titulo and recursos.fonte_pixel_numero:       
        COR_SOMBRA = (0, 0, 0) 

        # Transforma o número do score em texto (ex: 00000)
        texto_score_numero = f"{config.score:05d}" 
        
        # Cria os textos e as sombras
        hud_score_titulo = recursos.fonte_pixel_titulo.render("SCORE", True, (255, 0, 0))
        sombra_score_titulo = recursos.fonte_pixel_titulo.render("SCORE", True, COR_SOMBRA)
        
        hud_score_numero = recursos.fonte_pixel_numero.render(texto_score_numero, True, (255, 215, 0))
        sombra_score_numero = recursos.fonte_pixel_numero.render(texto_score_numero, True, COR_SOMBRA)

        # Posição do Score
        score_x = 1600 
        score_y = 70
        
        # Desenha o título "SCORE" com sombra
        tela.blit(sombra_score_titulo, (score_x + 2, score_y + 2))
        tela.blit(hud_score_titulo, (score_x, score_y))

        # Desenha os números da pontuação com sombra
        tela.blit(sombra_score_numero, (score_x + 2, score_y + 40 + 2))
        tela.blit(hud_score_numero, (score_x, score_y + 40))

    # Desenha o jogador
    jogador.desenhar(tela, sprite_mostrar)
    
    # Desenha o pinguim
    if recursos.sprites_pinguin_parado and sprite_inimigo_atual is not None and pinguim.vivo:
        if config.direcao_inimigo == "esquerda":
            sprite_inimigo_mostrar = pygame.transform.flip(sprite_inimigo_atual, True, False)
        else:
            sprite_inimigo_mostrar = sprite_inimigo_atual

        tela.blit(sprite_inimigo_mostrar, (pinguim.rect.x, pinguim.rect.y))

    # Desenha os tiros
    for tiro in config.projeteis:
        img_tiro = recursos.sprites_projeteis[tiro.tipo_sprite]
        if tiro.direcao == -1:
            img_tiro = pygame.transform.flip(img_tiro, True, False)
        tela.blit(img_tiro, (tiro.rect.x, tiro.rect.y))


    # DESENHAR NPC E BALÃO DE FALA

    if recursos.sprite_npc1 and config.indice_fundo == 0:
     tela.blit(recursos.sprite_npc1, (rect_npc.x, rect_npc.y))

     if config.perto_do_npc and not config.mostrar_balao:
            
            # Cria um efeito de pulsação
            oscilacao = (math.sin(pygame.time.get_ticks() * 0.005) + 1) / 2
            
            cor_r = int(255 * (0.5 + 0.5 * oscilacao))
            cor_g = int(215 * (0.5 + 0.5 * oscilacao))
            COR_DICA_PULSANTE = (cor_r, cor_g, 0)
            COR_SOMBRA_DICA = (0, 0, 0)
            
            texto_dica = recursos.fonte_dialogo.render("[T] INTERAGIR", True, COR_DICA_PULSANTE)
            sombra_dica = recursos.fonte_dialogo.render("[T] INTERAGIR", True, COR_SOMBRA_DICA)
            
            dica_x = rect_npc.x + (rect_npc.width // 2) - (texto_dica.get_width() // 2)
            dica_y = rect_npc.y - 35
            
            tela.blit(sombra_dica, (dica_x + 2, dica_y + 2))
            tela.blit(texto_dica, (dica_x, dica_y))


    if config.mostrar_balao:
            frase_atual = config.dialogo_npc1[config.indice_dialogo]
            NOME_NPC = "ARTHUR DUQUE"

            COR_FUNDO = (245, 245, 235)       # Bege bem clarinho/branco fosco
            COR_BORDA = (20, 20, 20)          # Quase preto para o contorno
            COR_SOMBRA_B = (140, 140, 130)    # Sombra do balão
            
            COR_TEXTO = (20, 20, 20)
            COR_SOMBRA_T = (180, 180, 180)
            COR_ETIQUETA = (255, 215, 0)

            # Renderiza o texto para medir o tamanho
            texto_fala = recursos.fonte_dialogo.render(frase_atual, True, COR_TEXTO)
            sombra_fala = recursos.fonte_dialogo.render(frase_atual, True, COR_SOMBRA_T)
            
            texto_nome = recursos.fonte_dialogo.render(NOME_NPC, True, COR_TEXTO)
            sombra_nome = recursos.fonte_dialogo.render(NOME_NPC, True, COR_SOMBRA_T)

            largura_texto, altura_texto = texto_fala.get_size()
            largura_nome, altura_nome = texto_nome.get_size()
            
            # Margens internasr
            margem_x = 20
            margem_y = 15
            
            largura_balao = largura_texto + (margem_x * 2)
            altura_balao = altura_texto + (margem_y * 2)
            
            # Posicionamento centralizado acima do NPC
            balao_x = rect_npc.x + (rect_npc.width // 2) - (largura_balao // 2)
            balao_y = rect_npc.y - altura_balao - 30
            
            
            pygame.draw.rect(tela, COR_SOMBRA_B, (balao_x + 4, balao_y + 4, largura_balao, altura_balao))
            pygame.draw.rect(tela, COR_BORDA, (balao_x, balao_y, largura_balao, altura_balao))
            pygame.draw.rect(tela, COR_FUNDO, (balao_x + 2, balao_y + 2, largura_balao - 4, altura_balao - 4))
            
            largura_etiqueta = largura_nome + 16
            altura_etiqueta = altura_nome + 8
            etiqueta_x = balao_x + 10  # Alinhado um pouco à esquerda no topo do balão
            etiqueta_y = balao_y - altura_etiqueta + 2  # Encaixado logo acima da borda
            
        
            pygame.draw.rect(tela, COR_BORDA, (etiqueta_x, etiqueta_y, largura_etiqueta, altura_etiqueta))
            pygame.draw.rect(tela, COR_ETIQUETA, (etiqueta_x + 2, etiqueta_y + 2, largura_etiqueta - 4, altura_etiqueta - 4))
            
            tela.blit(sombra_nome, (etiqueta_x + 9, etiqueta_y + 5))
            tela.blit(texto_nome, (etiqueta_x + 8, etiqueta_y + 4))

            setinha_x = rect_npc.x + (rect_npc.width // 2) - 6
            setinha_y = balao_y + altura_balao

            pygame.draw.rect(tela, COR_BORDA, (setinha_x, setinha_y, 12, 8))
            pygame.draw.rect(tela, COR_FUNDO, (setinha_x + 2, setinha_y, 8, 5))
            
            #DESENHANDO O TEXTO
            txt_x = balao_x + margem_x
            txt_y = balao_y + margem_y
            
            tela.blit(sombra_fala, (txt_x + 1, txt_y + 1))
            tela.blit(texto_fala, (txt_x, txt_y))


    # Desenha o chao 
    largura_bloco_chao = 100
    sprite_chao_ajustado = pygame.transform.scale(recursos.sprite_chao, (largura_bloco_chao + 1, config.chao.height))

    for x_atual in range(0, config.tamanho_tela[0], largura_bloco_chao):
        # O int() força o pixel a ser exato e o +1 fecha o vão (se tiver)
        tela.blit(sprite_chao_ajustado, (int(x_atual), config.chao.y))

    # Cursor para debug
    mx, my = pygame.mouse.get_pos()
    texto = fonte.render(f"X: {mx}, Y: {my}", True, (255, 255, 255))
    tela.blit(texto, (mx + 10, my - 20))


    pygame.display.flip()