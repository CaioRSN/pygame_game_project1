import pygame

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
  
        ],
        "blocos": [
           
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
