import pygame
import os
import pygame
# Inicialização necessária
pygame.init()
# Variáveis globais que começam vazias
sprite_tela_game_over = None
fundos = []
bloco_chao = None
sprite_personagem_scaled = None
sprites_parado = []
sprites_correndo = []
sprite_prepara_pulo = None
sprite_no_ar = None
sprite_caindo = None
sprites_atacando = []
sprites_projeteis = []
sprites_pinguin_parado = []
sprites_pinguin_andando = []
sprites_pinguin_atacando = []
sprites_personagem_pos_hit = []
sprites_pinguin_pos_hit = []
sprite_coracao = None
sprite_coracao_vazio = None
sprites_status_face = []
fonte_pixel_titulo = None
fonte_pixel_numero = None
fonte_game_over = None
fonte_hud_itens = None
sprites_blocos = []
sprites_plataformas = []
sprite_chao = None
sprite_bloco_inventario = None
sprite_itens = []
sprite_npc1 = None
sprite_balao_fala = None
fonte_dialogo = None
sprite_fundo_menu = None
item_energia_img = None
item_escudo_img = None
item_vida_img = None
sprite_efeito_vida = None
sprite_efeito_energia = None    
sprite_efeito_escudo = None
paginas_historia = []

def carregar_e_escalar(caminho, altura):
    img = pygame.image.load(caminho).convert_alpha()
    prop = img.get_width() / img.get_height()
    largura = int(altura * prop)
    return pygame.transform.scale(img, (largura, altura))

def inicializar_recursos(TAMANHO_TELA, ALTURA_PERSONAGEM):
    global sprite_bloco_inventario, fundos, bloco_chao, sprite_personagem_scaled, sprites_parado, sprites_correndo
    global sprite_prepara_pulo, sprite_no_ar, sprite_caindo, sprites_atacando, sprites_projeteis, sprite_coracao, sprite_coracao_vazio, sprites_status_face, sprites_personagem_pos_hit, sprites_pinguin_pos_hit
    global sprites_pinguin_parado, sprites_pinguin_andando, sprites_pinguin_atacando
    global sprite_npc1, sprite_balao_fala
    global fonte_pixel_titulo, fonte_pixel_numero, fonte_game_over, fonte_hud_itens, fonte_dialogo
    global sprites_blocos, sprites_plataformas, sprite_chao
    global paginas_historia, sprite_tela_game_over, sprite_fundo_menu, sprite_itens
    global item_energia_img, item_escudo_img, item_vida_img
    global sprite_efeito_vida, sprite_efeito_energia, sprite_efeito_escudo

   
    sprite_fundo_menu = pygame.transform.scale(
        pygame.image.load("imagens_e_texturas/tela_inicial.png").convert_alpha(),
        TAMANHO_TELA
    )
    sprite_tela_game_over = pygame.transform.scale(
        pygame.image.load("imagens_e_texturas/tela game over.png").convert_alpha(),
        TAMANHO_TELA
     )
    # --- CARREGAMENTO DOS FUNDOS ---
    fundos = [
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/cenario0.jpg"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/cenario1.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/cenario2.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/cenario3.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/cenario4.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/cenario5.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/cenario6.png"), TAMANHO_TELA),
    ]

    paginas_historia = [
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/historia1.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/historia2.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/historia3.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/historia4.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/historia5.png"), TAMANHO_TELA),
        pygame.transform.scale(pygame.image.load("imagens_e_texturas/historia6.png"), TAMANHO_TELA),
    ]

    #CHAO
    sprite_chao = pygame.image.load("imagens_e_texturas/chao-tijolinho.jpg").convert_alpha()
    #BLOCOS
    arquivos_blocos = [
        "png dos sprites/platf1 W.png", "png dos sprites/platf1 A.png", "png dos sprites/platf1 S.png", "png dos sprites/platf1 D.png"
    ]
        #tamanho padrão (50x50 pixels)
    sprites_blocos = [
        pygame.transform.scale(pygame.image.load(arq).convert_alpha(), (50, 50))
        for arq in arquivos_blocos
    ]
    #PLATAFORMAS
    arquivos_plataformas = [
        "png dos sprites/plat2 1.png", "png dos sprites/plat2 2.png"
    ]
   
    sprites_plataformas = [
        pygame.image.load(arq).convert_alpha()
        for arq in arquivos_plataformas
    ]
    # CARREGAMENTO DOS SPRITES DO JOGADOR
    sprite_base_personagem = pygame.image.load("png dos sprites/png lyoda.png")
    prop_base = sprite_base_personagem.get_width() / sprite_base_personagem.get_height()
    largura_final_base = int(ALTURA_PERSONAGEM * prop_base)
    sprite_personagem_scaled = pygame.transform.scale(sprite_base_personagem, (largura_final_base, ALTURA_PERSONAGEM))
    # Animação Parado
    lista_arquivos_parado = [
        "png dos sprites/parado1 1.png",
        "png dos sprites/parado1 2.png",
        "png dos sprites/parado1 4.png"
    ]
    sprites_parado = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in lista_arquivos_parado]
    # Animação Correndo
    arquivos_correndo = [
        "png dos sprites/corrida2 1.png",
        "png dos sprites/corrida2 2.png",
        "png dos sprites/corrida2 3.png",
        "png dos sprites/corrida2 4.png",
        "png dos sprites/corrida2 5.png",
        "png dos sprites/corrida2 6.png"
    ]
    sprites_correndo = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in arquivos_correndo]
    # Sprites de Pulo
    sprite_prepara_pulo = carregar_e_escalar("png dos sprites/prepulo1.png", ALTURA_PERSONAGEM)
    sprite_no_ar = carregar_e_escalar("png dos sprites/pulo1.png", ALTURA_PERSONAGEM)
    sprite_caindo = carregar_e_escalar("png dos sprites/pulo1.png", ALTURA_PERSONAGEM)
    # Animação Atacando
    arquivos_atacando = [
        "png dos sprites/ataque1 lyoda.png",
        "png dos sprites/ataque2 lyoda.png",
        "png dos sprites/ataque3 lyoda.png",
        "png dos sprites/ataque4 lyoda.png"
    ]
    sprites_atacando = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in arquivos_atacando]
    arquivo_personagem_pos_hit = [
        "png dos sprites/tomand hit1 1.png",
        "png dos sprites/tomand hit1 2.png",
        "png dos sprites/tomand hit1 3.png",
        "png dos sprites/tomand hit1 4.png",
        "png dos sprites/tomand hit1 5.png",
        "png dos sprites/tomand hit1 6.png",
        "png dos sprites/tomand hit1 7.png",
        "png dos sprites/tomand hit1 8.png",
         
    ]
    sprites_personagem_pos_hit = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in arquivo_personagem_pos_hit]
    arquivo_pinguin_pos_hit = [
        ]
    sprites_pinguin_pos_hit = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in arquivo_pinguin_pos_hit]
    # PROJÉTEIS
    sprites_projeteis = [
        pygame.transform.scale(pygame.image.load("png dos sprites/projetil tipo2 1.png").convert_alpha(), (120, 70)),
        pygame.transform.scale(pygame.image.load("png dos sprites/projetil tipo2 2.png").convert_alpha(), (120, 70))
    ]
   
    sprite_coracao = pygame.transform.scale(pygame.image.load("png dos sprites/coracao png.png").convert_alpha(), (35, 35))
    sprite_coracao_vazio = pygame.transform.scale(pygame.image.load("png dos sprites/coracao vazio png.png").convert_alpha(), (35, 35))
    # INIMIGO BASE PARADO
    arquivo_pinguin_parado = [
        "png dos sprites/pinguin inimigo1 1.png",
        "png dos sprites/pinguin inimigo1 2.png"  
   ]
    sprites_pinguin_parado = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in arquivo_pinguin_parado]
    arquivo_pinguin_andando = [
       "png dos sprites/pinguin inimigo and1.png",
       "png dos sprites/pinguin inimigo and2.png",
       "png dos sprites/pinguin inimigo and3.png",
       "png dos sprites/pinguin inimigo and4.png"
   ]
    sprites_pinguin_andando = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in arquivo_pinguin_andando]
    arquivo_pinguin_atacando = [
        "png dos sprites/pinguim attaq 1.png",
        "png dos sprites/pinguim attaq 2.png",
        "png dos sprites/pinguim attaq 3.png",
        "png dos sprites/pinguim attaq 4.png",
        "png dos sprites/pinguim attaq 5.png"
    ]
    sprites_pinguin_atacando = [carregar_e_escalar(arq, ALTURA_PERSONAGEM) for arq in arquivo_pinguin_atacando]
    #iCONE DA FACE
    rostos = [
        "icon face1 4.png"  
    ]
    sprites_status_face = [
        pygame.transform.scale(pygame.image.load(f"png dos sprites/{arq}").convert_alpha(), (120, 140))
        for arq in rostos
    ]
    fonte_pixel_titulo = pygame.font.Font("imagens_e_texturas/fonte tema do jogo.ttf", 32)
    fonte_pixel_numero = pygame.font.Font("imagens_e_texturas/fonte tema do jogo.ttf", 48)
    fonte_game_over = pygame.font.Font("imagens_e_texturas/fonte tema do jogo.ttf", 22)
    fonte_hud_itens = pygame.font.Font("imagens_e_texturas/fonte tema do jogo.ttf", 18)
    fonte_dialogo = pygame.font.Font("imagens_e_texturas/fonte tema do jogo.ttf", 16)
 
    sprite_bloco_inventario = pygame.image.load("png dos sprites/sprite_bloco_inventario.png").convert_alpha()
    sprite_bloco_inventario = pygame.transform.scale(sprite_bloco_inventario, (65, 65))
    sprite_item_cura = pygame.image.load("png dos sprites/sprite item de vida.png").convert_alpha()
    sprite_item_energia = pygame.image.load("png dos sprites/sprite item de energia.png").convert_alpha()
    sprite_item_escudo = pygame.image.load("png dos sprites/sprite item de escudo.png").convert_alpha()
    sprite_itens = [
        pygame.transform.scale(sprite_item_cura, (40, 40)),
        pygame.transform.scale(sprite_item_energia, (40, 40)),
        pygame.transform.scale(sprite_item_escudo, (40, 40))
    ]
    item_vida_img = sprite_itens[0]
    item_energia_img = sprite_itens[1]
    item_escudo_img = sprite_itens[2]
   
    sprite_npc1 = carregar_e_escalar("png dos sprites/duke parado1.png", ALTURA_PERSONAGEM)
    sprite_npc1 = pygame.transform.flip(sprite_npc1, True, False)
    sprite_balao_fala = pygame.image.load("png dos sprites/balao_fala.png").convert_alpha()
    #tamanho do balão
    sprite_balao_fala = pygame.transform.scale(sprite_balao_fala, (300, 100))

    sprite_efeito_vida = pygame.transform.scale(
        pygame.image.load("png dos sprites/sprite poder vida.png").convert_alpha(), (150, 150)  
    )
    sprite_efeito_energia = pygame.transform.scale(
        pygame.image.load("png dos sprites/sprite poder velocidade.png").convert_alpha(), (150, 150)
    )
    sprite_efeito_escudo = pygame.transform.scale(
        pygame.image.load("png dos sprites/sprite poder escudo.png").convert_alpha(), (150, 150)
    )

    return largura_final_base
# Configurações da tela e cores
tamanho_tela = (1920, 1080)
AZUL = (0, 0, 255)
# Posição inicial fixa e altura padrão
ALTURA_PERSONAGEM = 125
POS_X_INICIAL = 100
POS_Y_INICIAL = 500
# Variáveis de estado e controle do movimento
direcao = "direita"
velocidade_jogador = 4.5
# Chão e Plataformas
chao = pygame.Rect(0, 960, 1980, 120)
# --- SISTEMA DE FASES ---
fase_atual = 0
fases = {
    0: {
        "fundo_id": 0,
        "plataformas": [
    [pygame.Rect(1050, 850, 150, 50), 1],  
    [pygame.Rect(180, 300, 200, 70), 1],  
    [pygame.Rect(500, 400, 200, 70), 1],
    [pygame.Rect(1300, 750, 200, 70), 1],
    [pygame.Rect(1600, 650, 200, 70), 1],
    [pygame.Rect(900, 400, 200, 70), 1],
        ],
        "blocos": [
            [pygame.Rect(1430, 520, 50, 50), 0],
            [pygame.Rect(1220, 470, 50, 50), 0]
        ],
        "inimigo": {
            "pos_inicial": (1200, 835),
            "vida": 3,
            "vivo": True
        }   
    },
    1: {
        "fundo_id": 1,
        "plataformas": [
        [pygame.Rect(1400, 825, 150, 50), 1],
        [pygame.Rect(1600, 700, 150, 50), 1],
        ],
        "blocos": [
           
        ],
        "inimigo": None
    },
    }
# Variáveis dinâmicas que o jogo vai usar (elas mudam a cada troca de fase)
plataformas_flutuantes = fases[fase_atual]["plataformas"]
blocos_cenario = fases[fase_atual]["blocos"]
indice_fundo = fases[fase_atual]["fundo_id"]
# Atualiza a lista unificada de colisão inicial
plataformas = [p[0] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]
# Física do jogador
pulando = False      
velocidade_pulo = 18  
gravidade = 1        
velocidade_y = 0      
atacando = False
# Configurações de tempo e controle dos Projéteis
projeteis = []
indice_sprite_projetil = 0
ultimo_disparo = 0
cooldown_disparo = 3000
frame_atual = 0
# Controle do Loop
rodando = True
# Configurações do Inimigo
altura_inimigo = 125
inimigo_rect = pygame.Rect(1200, 835, 80, altura_inimigo)
frame_inimigo = 0
velocidade_anim_inimigo = 0.08
velocidade_inimigo = 2.5        
direcao_inimigo = "esquerda"  
vida_inimigo = 3
inimigo_vivo = True
vida_jogador = 5        
vida_maxima = 5        
frame_rosto = 0.0
velocidade_anim_rosto = 0.01
# --- Configurações do Timer ---
tempo_segundos = 0
contador_frames_tempo = 0
#MUDANCA DE FASE
def carregar_fase(numero_da_fase):
    global fase_atual, plataformas_flutuantes, blocos_cenario, indice_fundo, plataformas, inimigo_rect, vida_inimigo, inimigo_vivo
   
    # Garante que a fase existe no dicionário
    if numero_da_fase in fases:
        fase_atual = numero_da_fase
        plataformas_flutuantes = fases[fase_atual]["plataformas"]
        blocos_cenario = fases[fase_atual]["blocos"]
        indice_fundo = fases[fase_atual]["fundo_id"]
       
        # Recria a lista de colisões para a nova fase
        plataformas = [p[0] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]
        dados_inimigo = fases[fase_atual]["inimigo"]
        if dados_inimigo:
            x, y = dados_inimigo["pos_inicial"]
            inimigo_rect.x = x
            inimigo_rect.y = y
            vida_inimigo = dados_inimigo["vida"]
            inimigo_vivo = dados_inimigo["vivo"]
        else:
            # Se não tem inimigo nesta fase, marca como morto para sumir da tela e parar a IA do inimigo
            inimigo_vivo = False
