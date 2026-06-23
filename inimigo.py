import pygame
import config
import recursos

class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
<<<<<<< HEAD
        self.rect = pygame.Rect(1500, config.chao.y - config.ALTURA_PERSONAGEM, 80, config.ALTURA_PERSONAGEM)
        
        # Variáveis de estado INDIVIDUAIS do inimigo 
=======
        
        # Caixa de colisao e posicao inicial na tela
        self.rect = pygame.Rect(1500, config.chao.y - config.ALTURA_PERSONAGEM, 0, config.ALTURA_PERSONAGEM)
        
        # Garante a largura certa se a sprite ja estiver carregada
        if recursos.sprites_pinguin_parado:
            self.rect.width = recursos.sprites_pinguin_parado[0].get_width()
            
        # Variaveis de estado do bicho
>>>>>>> 6bf9d4e27b6ccccba47567619f2bc691bfc7553b
        self.vida = 3
        self.vivo = True
        self.movendo = False
        self.atacando = False
        self.frame = 0.0
        self.sprite_atual = None
<<<<<<< HEAD
        self.velocidade = 2.5  
        self.direcao = "esquerda" # Direção própria de cada instância
        
        self.estado = "parado"

    def atualizar_ia(self, jogador_rect):
=======

    def atualizar_ia(self, jogador_rect):
        # Se morreu, nao faz mais nada
>>>>>>> 6bf9d4e27b6ccccba47567619f2bc691bfc7553b
        if not self.vivo:
            self.sprite_atual = None
            return

<<<<<<< HEAD
        estado_anterior = self.estado

        self.movendo = False
        self.atacando = False

        # Se tiver em cooldown após bater no player
=======
        self.movendo = False
        self.atacando = False

        # Se tiver em cooldown apos bater no player, finge que esta longe
>>>>>>> 6bf9d4e27b6ccccba47567619f2bc691bfc7553b
        if config.tempo_descanso_inimigo > 0:
            config.tempo_descanso_inimigo -= 1
            distancia_x, distancia_y = 9999, 9999
        else:
            distancia_x = abs(jogador_rect.x - self.rect.x)
            distancia_y = abs(jogador_rect.y - self.rect.y)

<<<<<<< HEAD
        # IA do inimigo: Decide se ataca ou se persegue
        if distancia_x < 85 and distancia_y < 60:
            self.atacando = True
            self.direcao = "direita" if jogador_rect.x > self.rect.x else "esquerda"
        elif distancia_x < 600 and distancia_y < 200:
            if (jogador_rect.x - self.rect.x) > 15:
                self.rect.x += self.velocidade
                self.direcao = "direita"
                self.movendo = True
            elif (jogador_rect.x - self.rect.x) < -15:
                self.rect.x -= self.velocidade
                self.direcao = "esquerda"
                self.movendo = True

        # Escolhe as listas de animação e define o estado atual
        if self.atacando:
            self.estado = "atacando"
            lista_animacao = recursos.sprites_pinguin_atacando
            velocidade_anim = 0.15
        elif self.movendo:
            self.estado = "andando"
            lista_animacao = recursos.sprites_pinguin_andando
            velocidade_anim = 0.12
        else:
            self.estado = "parado"
            lista_animacao = recursos.sprites_pinguin_parado
            velocidade_anim = 0.05

        # Se mudou de estado em relação ao frame anterior, reseta a contagem de frames
        if self.estado != estado_anterior:
            self.frame = 0.0

        if lista_animacao:
            self.frame += velocidade_anim
            if self.frame >= len(lista_animacao):
                self.frame = 0.0
            
            sprite_base = lista_animacao[int(self.frame)]
            
            # Aplica o flip baseado na direção própria do pinguim
            if self.direcao == "esquerda":
                self.sprite_atual = pygame.transform.flip(sprite_base, True, False)
            else:
                self.sprite_atual = sprite_base
=======
        # Guarda o estado de antes para checar se mudou a animacao
        estado_anterior = "parado"
        if self.sprite_atual in recursos.sprites_pinguin_andando:
            estado_anterior = "andando"
        elif self.sprite_atual in recursos.sprites_pinguin_atacando:
            estado_anterior = "atacando"

        # IA: Decide se morde ou se corre atras
        if distancia_x < 80 and distancia_y < 50:
            self.atacando = True
        elif distancia_x < 500 and distancia_y < 150:
            # Margem de 15px pro bicho nao tremer parado
            if (jogador_rect.x - self.rect.x) > 15:
                self.rect.x += config.velocidade_inimigo
                config.direcao_inimigo = "direita"
                self.movendo = True
            elif (jogador_rect.x - self.rect.x) < -15:
                self.rect.x -= config.velocidade_inimigo
                config.direcao_inimigo = "esquerda"
                self.movendo = True

        # Escolhe as listas de animacao baseadas no estado
        if self.atacando:
            estado_novo = "atacando"
            lista_animacao = recursos.sprites_pinguin_atacando
            velocidade_anim = 0.15
        elif self.movendo:
            estado_novo = "andando"
            lista_animacao = recursos.sprites_pinguin_andando
            velocidade_anim = 0.12
        else:
            estado_novo = "parado"
            lista_animacao = recursos.sprites_pinguin_parado
            velocidade_anim = 0.05

        # Se o bicho mudou de estado, reseta a contagem de frames
        if estado_novo != estado_anterior:
            self.frame = 0.0

        # Roda a animacao e escolhe o sprite atual
        if lista_animacao:
            self.frame += velocidade_anim
            if self.frame >= len(lista_animacao):
                self.frame = 0
            self.sprite_atual = lista_animacao[int(self.frame)]
>>>>>>> 6bf9d4e27b6ccccba47567619f2bc691bfc7553b
