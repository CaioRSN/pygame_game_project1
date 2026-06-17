import pygame
from cenario import Cenario

tamanho_tela = (1920, 1080)
AZUL = (0, 0, 255)

ALTURA_PERSONAGEM = 125
POS_X_INICIAL = 100
POS_Y_INICIAL = 500

direcao = "direita"
velocidade_jogador = 4.5

chao = pygame.Rect(0, 960, 1980, 120)

# --- SISTEMA DE FASES USANDO A CLASSE ---
fase_atual = 0

fases = {
    0: Cenario(
        indice_fundo=0,
        plataformas=[],
        blocos=[]
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
            [pygame.Rect(1220, 470, 50, 50), 0]
        ]
    )
}

# Inicializa as variáveis dinâmicas com a fase 0
plataformas_flutuantes = fases[fase_atual].plataformas_flutuantes
blocos_cenario = fases[fase_atual].blocos_cenario
indice_fundo = fases[fase_atual].indice_fundo

plataformas = [p[0] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]

pulando = False       
velocidade_pulo = 18  
gravidade = 1         
velocidade_y = 0      
atacando = False

projeteis = []
indice_sprite_projetil = 0 
ultimo_disparo = 0
cooldown_disparo = 3000 
frame_atual = 0

rodando = True

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

tempo_segundos = 0
contador_frames_tempo = 0

score = 0

# Quantidade inicial de cada um dos 3 itens
inventario_quantidades = {
    "item_1": 0,
    "item_2": 0,
    "item_3": 0,
}



dialogo_npc1 = [
    "PROFESSOR???!!!",
    "Acho que exagerei nos tickets e abri esse portal...",
    "Os pinguins estao fora de controle!",
    "Por favor, use suas habilidades 'programalisticas'...",
    "para derrota-los e salvar o nosso tão amado CIN!",
]


# Variáveis de controle do sistema de diálogo
indice_dialogo = 0       # Qual frase está aparecendo agora
mostrar_balao = False    # Controla se o balão deve ser desenhado na tela
perto_do_npc = False     # Sabe se o jogador está colado no NPC


# Função que gerencia a transição chamando a classe
def carregar_fase(numero_da_fase):
    global fase_atual, plataformas_flutuantes, blocos_cenario, indice_fundo, plataformas
    
    if numero_da_fase in fases:
        fase_atual = numero_da_fase
        
        # Carrega os dados do objeto Cenario correspondente
        fases[fase_atual].carregar()
        
        plataformas_flutuantes = fases[fase_atual].plataformas_flutuantes
        blocos_cenario = fases[fase_atual].blocos_cenario
        indice_fundo = fases[fase_atual].indice_fundo
        
        plataformas = [p[0] for p in plataformas_flutuantes] + [b[0] for b in blocos_cenario]