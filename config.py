import pygame
from cenario import Cenario
from inimigo import Inimigo

tamanho_tela = (1920, 1080)
AZUL = (0, 0, 255)
ALTURA_PERSONAGEM = 125
POS_X_INICIAL = 100
POS_Y_INICIAL = 500
direcao = "direita"
velocidade_jogador = 20  # Velocidade inicial atualizada

chao = pygame.Rect(0, 960, 1980, 120)

# --- Inimigos da Fase 0 (Cenário 0) ---
pinguim_f0 = Inimigo()
pinguim_f0.rect.x = 1500

# --- Inimigos da Fase 1 (Cenário 1) ---
p1_f1 = Inimigo()
p1_f1.rect.x = 800
p2_f1 = Inimigo()
p2_f1.rect.x = 1300

# --- Inimigos da Fase 2 (Cenário 2) ---
p1_f2 = Inimigo()
p1_f2.rect.x = 600
p2_f2 = Inimigo()
p2_f2.rect.x = 1400

# --- Inimigos da Fase 3 (Cenário 3) ---
p1_f3 = Inimigo()
p1_f3.rect.x = 1100
p2_f3 = Inimigo()
p2_f3.rect.x = 1600

# --- Inimigos da Fase 4 (Cenário 4) ---
p1_f4 = Inimigo()
p1_f4.rect.x = 900
p2_f4 = Inimigo()
p2_f4.rect.x = 1400

# --- Inimigos da Fase 5 (Cenário 5) ---
p1_f5 = Inimigo()
p1_f5.rect.x = 600  
p2_f5 = Inimigo()
p2_f5.rect.x = 1400

# --- Inimigos da Fase 6 (Cenário 6) ---
p1_f6 = Inimigo()
p1_f6.rect.x = 600
p2_f6 = Inimigo()
p2_f6.rect.x = 1400

# --- Inimigos da Fase 7 (Cenário 7) ---
p1_f7 = Inimigo()
p1_f7.rect.x = 500  
p2_f7 = Inimigo()
p2_f7.rect.x = 1300


fase_atual = 0
fases = {
    0: Cenario(
        indice_fundo=0,
        plataformas=[],
        blocos=[],
        inimigos=[pinguim_f0]
    ),
    1: Cenario(
        indice_fundo=1,
        plataformas=[
            [pygame.Rect(1050, 850, 150, 50), 1],
            [pygame.Rect(180, 300, 200, 70), 1],
            [pygame.Rect(500, 400, 200, 70), 1],
            [pygame.Rect(1300, 750, 200, 70), 1],
            [pygame.Rect(1600, 650, 200, 70), 1],
            [pygame.Rect(900, 400, 200, 70), 1],
        ],
        blocos=[
            [pygame.Rect(1430, 520, 50, 50), 0],
            [pygame.Rect(1220, 470, 50, 50), 0],
        ],
        inimigos=[p1_f1, p2_f1]
    ),
    2: Cenario(
        indice_fundo=2,
        plataformas=[
            [pygame.Rect(200, 830, 200, 50), 1],
            [pygame.Rect(500, 710, 200, 50), 1],
            [pygame.Rect(800, 590, 200, 50), 1],
            [pygame.Rect(1100, 640, 200, 50), 1],
            [pygame.Rect(1400, 520, 200, 50), 1],
        ],
        blocos=[], 
        inimigos=[p1_f2, p2_f2]
    ),
    3: Cenario(
        indice_fundo=3,
        plataformas=[
            [pygame.Rect(150, 830, 200, 60), 1],
            [pygame.Rect(450, 710, 200, 60), 1],
            [pygame.Rect(750, 590, 250, 60), 1],
            [pygame.Rect(1100, 650, 200, 60), 1],
            [pygame.Rect(1400, 720, 200, 60), 1],
            [pygame.Rect(1650, 600, 200, 60), 1],
        ],
        blocos=[],
        inimigos=[p1_f3, p2_f3]
    ),
    4: Cenario(
        indice_fundo=4,
        plataformas=[
            [pygame.Rect(150, 720, 220, 50), 1],
            [pygame.Rect(450, 590, 200, 50), 1],
            [pygame.Rect(900, 480, 180, 50), 1],
            [pygame.Rect(1300, 590, 200, 50), 1],
            [pygame.Rect(1580, 720, 220, 50), 1],
        ],
        blocos=[
            [pygame.Rect(230, 850, 60, 110), 0],
            [pygame.Rect(1660, 850, 60, 110), 0],
            [pygame.Rect(670, 530, 60, 110), 0]
        ],
        inimigos=[p1_f4, p2_f4]
    ),
    5: Cenario(
        indice_fundo=5,  
        plataformas=[
            [pygame.Rect(150, 720, 220, 50), 1],
            [pygame.Rect(450, 590, 200, 50), 1],
            [pygame.Rect(750, 480, 180, 50), 1],
            [pygame.Rect(1020, 480, 180, 50), 1],
            [pygame.Rect(1300, 590, 200, 50), 1],
            [pygame.Rect(1580, 720, 220, 50), 1],
        ],
        blocos=[
            [pygame.Rect(230, 850, 60, 110), 0],
            [pygame.Rect(1660, 850, 60, 110), 0],
        ],
        inimigos=[p1_f5, p2_f5]  
    ),
    6: Cenario(
        indice_fundo=6,
        plataformas=[
            [pygame.Rect(150, 830, 200, 60), 1],
            [pygame.Rect(450, 710, 200, 60), 1],
            [pygame.Rect(750, 590, 250, 60), 1],
            [pygame.Rect(1100, 390, 200, 60), 1],
            [pygame.Rect(1400, 720, 200, 60), 1],
            [pygame.Rect(1650, 600, 200, 60), 1],
        ],
        blocos=[],
        inimigos=[p1_f6, p2_f6] if 'p1_f6' in locals() else [Inimigo(), Inimigo()]
    ), 
    7: Cenario(
        indice_fundo=7,
        plataformas=[
            
        ],
        blocos=[
            
        ],
       inimigos=[
           
       ]
    ),
}

# Inicializa as variáveis dinâmicas com a fase 0
plataformas_flutuantes = fases[fase_atual].plataformas_flutuantes
blocos_cenario = fases[fase_atual].blocos_cenario
indice_fundo = fases[fase_atual].indice_fundo
inimigos_cenario = fases[fase_atual].inimigos
plataformas = [p["rect"] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]

pulando = False
velocidade_pulo = 20
gravidade = 1
velocidade_y = 0
atacando = False
projeteis = False
projeteis = []
indice_sprite_projetil = 0
ultimo_disparo = 0
cooldown_disparo = 1500
frame_atual = 0
rodando = True

jogo_vencido = False

# Definições gerais do inimigo
altura_inimigo = 125
inimigo_rect = pygame.Rect(1200, 835, 80, altura_inimigo)
frame_inimigo = 0
velocidade_anim_inimigo = 0.1
velocidade_inimigo = 2.5
direcao_inimigo = "esquerda"
vida_inimigo = 3
inimigo_vivo = True

vida_jogador = 5
vida_maxima = 5
frame_rosto = 0.0
velocidade_anim_rosto = 0.01
tempo_segundos = 0
contador_frames_tempo = 0
score = 0

inventario = {
    "energia": 0,
    "escudo": 0,
    "vida": 0,
    "cracha": 0  
}

# Variável global de controle para adicionar logo abaixo do inventário
crachas_gerados_na_fase = False

# Sistema de Diálogo do NPC
dialogo_npc1 = [
    "PROFESSOR???!!!",
    "Acho que exagerei nos tickets e abri esse portal...",
    "Os pinguins estao fora de controle!",
    "Por favor, use suas habilidades 'programalisticas'...",
    "para derrota-los e salvar o nosso tão amado CIN!"
]
indice_dialogo = 0
mostrar_balao = False
perto_do_npc = False
no_menu = False

def carregar_fase(numero_da_fase):
    global fase_atual, plataformas_flutuantes, blocos_cenario, indice_fundo, plataformas, inimigos_cenario, crachas_gerados_na_fase
    if numero_da_fase in fases:
        fase_atual = numero_da_fase
        fases[fase_atual].carregar()
        plataformas_flutuantes = fases[fase_atual].plataformas_flutuantes
        blocos_cenario = fases[fase_atual].blocos_cenario
        indice_fundo = fases[fase_atual].indice_fundo
        inimigos_cenario = fases[fase_atual].inimigos
        
        # Garante o reset global para liberar o spawn na nova fase
        crachas_gerados_na_fase = False
        
        # Garante a leitura compatível de dicionários para plataformas e listas para blocos
        plataformas = [p["rect"] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]
        
        

# ----- MOVIMENTAÇÃO DAS PLATAFORMAS -----
velocidade_plataforma = 2
direcao_plataforma = 1
posicoes_iniciais_plataformas = {}

def atualizar_movimento_plataformas(fase_alvo, indice_plataforma, jogador_instancia, afastamento_maximo=150, velocidade=2):
    if fase_atual == fase_alvo:
        plataformas_flutuantes = fases[fase_atual].plataformas_flutuantes
        
        if 0 <= indice_plataforma < len(plataformas_flutuantes):
            plat = plataformas_flutuantes[indice_plataforma]["rect"]
            
            chave_x = f"fase{fase_alvo}_plat{indice_plataforma}_x"
            chave_dir = f"fase{fase_alvo}_plat{indice_plataforma}_dir"
            
            if chave_x not in posicoes_iniciais_plataformas:
                posicoes_iniciais_plataformas[chave_x] = plat.x
                posicoes_iniciais_plataformas[chave_dir] = 1 
            
            x_original = posicoes_iniciais_plataformas[chave_x]
            direcao_atual = posicoes_iniciais_plataformas[chave_dir]
            
            limite_esquerdo = x_original - afastamento_maximo
            limite_direito = x_original + afastamento_maximo
            
            deslocamento_x = velocidade * direcao_atual
            plat.x += deslocamento_x
            
            # Movimentação do jogador (usando o parâmetro que veio da chamada da main)
            colisao_horizontal = (jogador_instancia.rect.right > plat.left and jogador_instancia.rect.left < plat.right)
            no_topo = abs(jogador_instancia.rect.bottom - plat.top) <= 12
            
            if colisao_horizontal and no_topo and not jogador_instancia.pulando:
                jogador_instancia.rect.x += deslocamento_x

            if plat.x >= limite_direito:
                posicoes_iniciais_plataformas[chave_dir] = -1
            elif plat.x <= limite_esquerdo:
                posicoes_iniciais_plataformas[chave_dir] = 1

            global plataformas
            plataformas = [p["rect"] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]

def atualizar_movimento_vertical_plataformas(fase_alvo, indice_plataforma, jogador_instancia, afastamento_maximo=150, velocidade=2):
    if fase_atual == fase_alvo:
        plataformas_flutuantes = fases[fase_atual].plataformas_flutuantes
        
        if 0 <= indice_plataforma < len(plataformas_flutuantes):
            plat = plataformas_flutuantes[indice_plataforma]["rect"]
            
            chave_y = f"fase{fase_alvo}_plat{indice_plataforma}_y"
            chave_dir_v = f"fase{fase_alvo}_plat{indice_plataforma}_dir_v"
            
            if chave_y not in posicoes_iniciais_plataformas:
                posicoes_iniciais_plataformas[chave_y] = plat.y
                posicoes_iniciais_plataformas[chave_dir_v] = 1 
            
            y_original = posicoes_iniciais_plataformas[chave_y]
            direcao_atual = posicoes_iniciais_plataformas[chave_dir_v]
            
            limite_superior = y_original - afastamento_maximo
            limite_inferior = y_original + afastamento_maximo
            
            deslocamento_y = velocidade * direcao_atual
            plat.y += deslocamento_y
            
            # Movimentação do jogador no eixo Y (usando o parâmetro)
            colisao_horizontal = (jogador_instancia.rect.right > plat.left and jogador_instancia.rect.left < plat.right)
            no_topo = abs(jogador_instancia.rect.bottom - plat.top) <= 12
            
            if colisao_horizontal and no_topo and not jogador_instancia.pulando:
                jogador_instancia.rect.bottom = plat.top

            if plat.y >= limite_inferior:
                posicoes_iniciais_plataformas[chave_dir_v] = -1
            elif plat.y <= limite_superior:
                posicoes_iniciais_plataformas[chave_dir_v] = 1

            global plataformas
            plataformas = [p["rect"] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]
