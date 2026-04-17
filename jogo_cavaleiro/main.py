import pygame
pygame.init()

    #Configurações da tela
tamanho_tela = (1980, 1080)  
tela = pygame.display.set_mode(tamanho_tela)
pygame.display.set_caption("Cin aventure")


    # Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)


fundos = [
    pygame.transform.scale(pygame.image.load("imagens_e_texturas/background 2.jpg"), tamanho_tela),
    pygame.transform.scale(pygame.image.load("imagens_e_texturas/background 2-2.jpg"), tamanho_tela),
    pygame.transform.scale(pygame.image.load("imagens_e_texturas/background 2-3.jpg"), tamanho_tela)
]


    #Variáveis do jogador
altura_do_personagem = 125
sprite_personagem = pygame.image.load("png dos sprites/png lyoda.png")


def carregar_e_escalar(caminho, altura):
    #Carrega a imagem
    img = pygame.image.load(caminho).convert_alpha()
    #Calcula a proporção (largura / altura)
    prop = img.get_width() / img.get_height()
    #Calcula a largura final baseada na altura desejada
    largura = int(altura * prop)
    #Retorna a imagem redimensionada
    return pygame.transform.scale(img, (largura, altura))


#calculo da proporção
largura_original = sprite_personagem.get_width()
altura_original = sprite_personagem.get_height()
proporcao = largura_original / altura_original
largura_final = int(altura_do_personagem * proporcao)

personagem_sprite = pygame.transform.scale(sprite_personagem, (largura_final, altura_do_personagem))

tamanho_jogador = altura_do_personagem
jogador = pygame.Rect(100, 500, largura_final, altura_do_personagem)



direcao = "direita"

velocidade_jogador = 6  # velocidade de movimento


    #Plataforma e chão
largura_chao = 1980
altura_chao = 100
chao = pygame.Rect(0, 960, largura_chao, altura_chao)

textura_chao = pygame.image.load("imagens_e_texturas/texturachao 2.png") #textura chao
largura_textura = textura_chao.get_width()   # largura da imagem em pixels
altura_textura = textura_chao.get_height()   # altura da imagem em pixels

bloco_chao = pygame.transform.scale(textura_chao, (100, altura_chao))  # feito só uma vez
largura_textura = bloco_chao.get_width()




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



atacando = False
duracao_ataque = 12



    #Loop principal
clock = pygame.time.Clock()
rodando = True



   #animacoes
   #Configurações da Animação
lista_arquivos_parado = [
    "png dos sprites/lyoda parado 1.png",
    "png dos sprites/lyoda parado 2.png",
    "png dos sprites/lyoda parado 3.png",
    "png dos sprites/lyoda parado 3.png"
]

sprites_parado = []

for arquivo in lista_arquivos_parado:
    img = pygame.image.load(arquivo).convert_alpha()
    
    # Calcula a proporção individual de cada frame
    larg_orig = img.get_width()
    alt_orig = img.get_height()
    prop = larg_orig / alt_orig
    larg_frame = int(altura_do_personagem * prop)
    
    # Redimensiona mantendo a proporção daquele frame específico
    img_redimensionada = pygame.transform.scale(img, (larg_frame, altura_do_personagem))
    sprites_parado.append(img_redimensionada)

frame_atual = 0
velocidade_animacao = 0.025  

    #animacoes correndo
arquivos_correndo = [
    "png dos sprites/lyoda correndo 1.png",
    "png dos sprites/lyoda correndo 2.png",
    "png dos sprites/lyoda correndo 3.png",
    "png dos sprites/lyoda correndo 4.png"
]

sprites_correndo = []
for arquivo in arquivos_correndo:
    img = pygame.image.load(arquivo).convert_alpha()
    # Mantém a proporção baseada na altura
    prop = img.get_width() / img.get_height()
    larg_frame = int(altura_do_personagem * prop)
    img_redimensionada = pygame.transform.scale(img, (larg_frame, altura_do_personagem))
    sprites_correndo.append(img_redimensionada)



# Chamando a função para cada sprite de ação
sprite_prepara_pulo = carregar_e_escalar("png dos sprites/lyoda preparando pulo.png", altura_do_personagem)
sprite_no_ar = carregar_e_escalar("png dos sprites/lyoda pulando 1.png", altura_do_personagem)
sprite_caindo = carregar_e_escalar("png dos sprites/lyoda caindo 1.png", altura_do_personagem)


#ataque e disparos
# Pose do Lyoda disparando (tipo Cuphead)
sprite_pose_disparo = carregar_e_escalar("png dos sprites/lyoda atirando 1.png", altura_do_personagem)


#fade do background
indice_fundo = 0
proximo_fundo = 1
alpha = 0
velocidade_fade = 5  # quanto maior, mais rápido troca
tempo_troca = 300  # 3 segundos
ultimo_tempo = pygame.time.get_ticks()


# Lista de sprites de projétil
sprites_projeteis = [
    pygame.transform.scale(pygame.image.load("png dos sprites/projetil 1 lyoda.png").convert_alpha(), (30, 30)),
    pygame.transform.scale(pygame.image.load("png dos sprites/projetil 2 lyoda.png").convert_alpha(), (30, 30))
]

projeteis = []
indice_sprite_projetil = 0 # Qual projétil usar agora (0 ou 1)
ultimo_disparo = 0
cooldown_disparo = 300 # Milissegundos


while rodando:
    clock.tick(60)
    
    # Mova as definições de tempo e teclas para o topo do loop
    tempo_atual = pygame.time.get_ticks()
    teclas = pygame.key.get_pressed() 

    # Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_SPACE and not pulando:
                velocidade_y = -velocidade_pulo
                pulando = True

    # Agora a variável 'teclas' e 'tempo_atual' já existem 
    # e podem ser usadas aqui embaixo sem erro:
    
# Lógica de disparo
        if teclas[pygame.K_k]:
            atacando = True
            if tempo_atual - ultimo_disparo > cooldown_disparo:
                pos_x = jogador.right if direcao == "direita" else jogador.left - 30
                
                novo_tiro = {
                    "rect": pygame.Rect(pos_x, jogador.centery, 30, 30),
                    "tipo_sprite": indice_sprite_projetil,
                    "direcao": 1 if direcao == "direita" else -1
                }
                
                projeteis.append(novo_tiro)
                
                indice_sprite_projetil = 1 - indice_sprite_projetil
                ultimo_disparo = tempo_atual
    else:
        atacando = False

#Atualizar posição dos tiros
        for tiro in projeteis[:]:
            tiro["rect"].x += 15 * tiro["direcao"]
            if tiro["rect"].x < 0 or tiro["rect"].x > 1980:
                projeteis.remove(tiro)

        # 2. Movimento (Só acontece se NÃO estiver atacando)
        movendo = False 
        if not atacando:
            # Esquerda (Setinha ou A)
            if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
                jogador.x -= velocidade_jogador
                direcao = "esquerda"
                movendo = True
            
            # Direita (Setinha ou D)
            if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
                jogador.x += velocidade_jogador
                direcao = "direita"
                movendo = True


            # Pulo (Setinha Cima, W ou Espaço)
            if (teclas[pygame.K_SPACE] or teclas[pygame.K_w] or teclas[pygame.K_UP]) and not pulando:
                velocidade_y = -velocidade_pulo
                pulando = True



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
        


# Lógica de Animação
        if atacando:
            personagem_sprite = sprite_pose_disparo
            frame_atual = 0
        elif pulando:
            frame_atual = 0 
            if velocidade_y < -5:
                personagem_sprite = sprite_prepara_pulo
            elif -5 <= velocidade_y <= 5:
                personagem_sprite = sprite_no_ar
            else:
                personagem_sprite = sprite_caindo
        else:
            # Lógica de chão (Parado ou Correndo)
            if movendo:
                lista_atual = sprites_correndo
                velocidade_anim_atual = 0.1 
            else:
                lista_atual = sprites_parado
                velocidade_anim_atual = 0.025 

            frame_atual += velocidade_anim_atual
            if frame_atual >= len(lista_atual):
                frame_atual = 0
            
            personagem_sprite = lista_atual[int(frame_atual)]


        # Desenhar na tela zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz
        if direcao == "esquerda":
         sprite_mostrar = pygame.transform.flip(personagem_sprite, True, False)  # vira horizontalmente
        else:
         sprite_mostrar = personagem_sprite  # mantém normal
        
        
        tempo_atual = pygame.time.get_ticks()

        #começa a transição depois de um tempo
        if tempo_atual - ultimo_tempo > tempo_troca:
         alpha += velocidade_fade

         if alpha >= 255:
          alpha = 0
          indice_fundo = proximo_fundo
          proximo_fundo = (proximo_fundo + 1) % len(fundos)
          ultimo_tempo = tempo_atual


        # Desenhar na tela
        # 1. Desenha o Fundo primeiro (ele é a camada de trás)
        # fundo atual
        tela.blit(fundos[indice_fundo], (0, 0))

         #fundo próximo com transparência
        fundo_temp = fundos[proximo_fundo].copy()
        fundo_temp.set_alpha(alpha)
        tela.blit(fundo_temp, (0, 0))

        # 2. Desenha o restante (chão, plataformas, jogador)

        for plataforma in plataformas:
            pygame.draw.rect(tela, AZUL, plataforma)

        pos_x_centralizado = jogador.centerx - (sprite_mostrar.get_width() // 2)
        tela.blit(sprite_mostrar, (pos_x_centralizado, jogador.y))
        
        
        #3. Desenhar projéteis
        for tiro in projeteis:
            img_tiro = sprites_projeteis[tiro["tipo_sprite"]]
            
            if tiro["direcao"] == -1:
                img_tiro = pygame.transform.flip(img_tiro, True, False)
                
            tela.blit(img_tiro, (tiro["rect"].x, tiro["rect"].y))

    
        pygame.display.flip()

    #zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz

pygame.quit()
