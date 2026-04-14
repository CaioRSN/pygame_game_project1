import pygame
pygame.init()

    # --- Configurações da tela ---
tamanho_tela = (1980, 1080)  # resolvi diminuir para ficar mais fácil de testar
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("A Knight Adventure")

    # --- Cores ---
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

    # --- Carregar Fundo ---
fundo_original = pygame.image.load("imagens_e_texturas/background.jpg")
fundo = pygame.transform.scale(fundo_original, tamanho_tela)

    # --- Variáveis do jogador ---
tamanho_jogador = 50
jogador = pygame.Rect(100, 500, tamanho_jogador, tamanho_jogador)  # posição inicial
sprite_personagem = pygame.image.load("imagens_e_texturas/sprite_personagem png.png")
personagem_sprite = pygame.transform.scale(sprite_personagem, (tamanho_jogador, tamanho_jogador))

direcao = "direita"

velocidade_jogador = 7  # velocidade de movimento

    # --- Plataforma e chão ---
largura_chao = 1980
altura_chao = 100
chao = pygame.Rect(0, 920, largura_chao, altura_chao)

textura_chao = pygame.image.load("imagens_e_texturas/texturachao 2.png") #textura chao
largura_textura = textura_chao.get_width()   # largura da imagem em pixels
altura_textura = textura_chao.get_height()   # altura da imagem em pixels

bloco_chao = pygame.transform.scale(textura_chao, (100, altura_chao))  # feito só uma vez
largura_textura = bloco_chao.get_width()

    # Você pode adicionar mais plataformas, se quiser
plataformas = [
    pygame.Rect(150, 400, 200, 20),
    pygame.Rect(450, 300, 150, 20),
    pygame.Rect(850, 850, 200, 20),
    pygame.Rect(800, 750, 150, 20),
    pygame.Rect(600, 650, 250, 20),
    pygame.Rect(500, 550, 150, 20)
        ]
    
    #pulo do jogador
    # Estado do pulo
pulando = False       # indica se o jogador está no ar
velocidade_pulo = 18  # força do pulo
gravidade = 1         # gravidade constante
velocidade_y = 0      # velocidade vertical do jogador

    #attaque
sprite_ataque = pygame.image.load("imagens_e_texturas/sprit attack.png")
ataque_sprite = pygame.transform.scale(sprite_ataque, (250, 50))

atacando = False
timer_ataque = 0
duracao_ataque = 12

    # --- Loop principal ---
clock = pygame.time.Clock()
rodando = True

while rodando:
        clock.tick(60)  # 60 FPS

        # --- Eventos ---
        
    # --- Eventos ---
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.KEYDOWN:
                # Pulo
                if evento.key == pygame.K_SPACE and not pulando:
                    velocidade_y = -velocidade_pulo
                    pulando = True
                
                # Ataque (Aciona o estado de ataque)
                if evento.key == pygame.K_z and not atacando:
                    atacando = True
                    timer_ataque = duracao_ataque
        
        # Lógica do timer de ataque (faz o ataque sumir depois de um tempo)
        if atacando:
            timer_ataque -= 1
            if timer_ataque <= 0:
                atacando = False

        # --- Movimento do jogador ---
        teclas = pygame.key.get_pressed()

        if teclas[pygame.K_LEFT]:
         jogador.x -= velocidade_jogador
         direcao = "esquerda"  # atualiza direção

        if teclas[pygame.K_RIGHT]:
         jogador.x += velocidade_jogador
         direcao = "direita"  # atualiza direção

        #pulo
        if teclas[pygame.K_SPACE] and not pulando:
         velocidade_y = -velocidade_pulo  # sobe
         pulando = True                    # jogador está no ar

        #Aplica gravidade
        velocidade_y += gravidade
        jogador.y += velocidade_y
    
        #Checa colisão com o chão
        if jogador.colliderect(chao) and velocidade_y >= 0:
         jogador.bottom = chao.top
         velocidade_y = 0
         pulando = False

        # Checa colisão com plataformas
        for plataforma in plataformas:
         if jogador.colliderect(plataforma) and velocidade_y >= 0:
            if jogador.bottom - velocidade_y <= plataforma.top:  # estava acima antes de mover
                jogador.bottom = plataforma.top
                velocidade_y = 0
                pulando = False        

        # --- Desenhar na tela zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
        if direcao == "esquerda":
         sprite_mostrar = pygame.transform.flip(personagem_sprite, True, False)  # vira horizontalmente
        else:
         sprite_mostrar = personagem_sprite  # mantém normal
        
        # --- Desenhar na tela ---
        # 1. Desenha o Fundo primeiro (ele é a camada de trás)
        tela.blit(fundo, (0, 0))

        # 2. Desenha o restante (chão, plataformas, jogador)
        for i in range(0, chao.width, largura_textura):
            tela.blit(bloco_chao, (chao.x + i, chao.y))


        for i in range(0, chao.width, largura_textura):
         tela.blit(bloco_chao, (chao.x + i, chao.y))
        for plataforma in plataformas:
            pygame.draw.rect(tela, PRETO, plataforma)

        tela.blit(sprite_mostrar, (jogador.x, jogador.y))

        # --- Desenhar o Ataque ---
        if atacando:
            if direcao == "direita":
                # Posiciona na frente do jogador (x + largura)
                pos_x_ataque = (jogador.x + tamanho_jogador) - 125 
                ataque_final = ataque_sprite
            else:
                # Posiciona atrás do jogador e inverte a imagem
                pos_x_ataque = (jogador.x - 125) 
                ataque_final = pygame.transform.flip(ataque_sprite, True, False)
            
            pos_y_ataque = jogador.y - 25 
            # Desenha o sprite na tela (ajuste jogador.y se ficar muito alto)
            tela.blit(ataque_final, (pos_x_ataque, jogador.y))

        pygame.display.flip()

    #zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

pygame.quit()
