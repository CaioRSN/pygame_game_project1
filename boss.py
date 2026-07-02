import pygame
import random
import config
import recursos

class Boss(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Começa grande e vermelho no canto direito da tela
        self.rect = pygame.Rect(1500, config.chao.y - 400, 300, 400) 
        self.frame = 0.0
        self.sprite_atual = None
        self.direcao = "esquerda"
        
        
        self.vida_maxima = 10
        self.vida = 10
        self.vivo = True
        self.cor = (255, 0, 0)

        # Estados: 'descanso', 'prepara_pulo', 'pulo', 'ataque_chao'
        self.estado = 'descanso'
        self.timer_estado = 60 # Frames para a próxima ação
        
        # Variáveis auxiliares para os ataques
        self.velocidade_y = 0
        self.alvo_x = 0
        self.subindo = False

        self.rect_trampolim = pygame.Rect(0, 0, 0, 0)
        self.trampolim_ativo = False

    def atualizar(self, jogador_rect):
        if not self.vivo:
            return

        #a animação do modo descanso
        if self.estado == 'descanso' and recursos.sprites_boss_parado:
            self.frame += 0.05  # Velocidade da animação 
            if self.frame >= len(recursos.sprites_boss_parado):
                self.frame = 0.0

            sprite_base = recursos.sprites_boss_parado[int(self.frame)]

            # Define para onde o Boss deve olhar baseado na posição do jogador
            self.direcao = "direita" if jogador_rect.x > self.rect.x else "esquerda"

            if self.direcao == "esquerda":
                self.sprite_atual = pygame.transform.flip(sprite_base, True, False)
            else:
                self.sprite_atual = sprite_base
        else:
            # Por enquanto, mantém o retângulo mudando de cor nos ataques
            self.sprite_atual = None


        # ESTADO: DESCANSO (Esperando para atacar)
        if self.estado == 'descanso':
            self.timer_estado -= 1
            if self.timer_estado <= 0:
                self.estado = random.choice(['prepara_pulo', 'ataque_chao'])
                if self.estado == 'ataque_chao':
                    self.timer_estado = 100 #tempo para o jogador ver o trampolim e correr
                else:
                    self.timer_estado = 20

       # ATAQUE 1: PULO 
        elif self.estado == 'prepara_pulo':
            self.timer_estado -= 1
            
            # Sprite se preparando
            if "prepara" in recursos.sprites_boss_pulo:
                sprite_base = recursos.sprites_boss_pulo["prepara"]
                self.sprite_atual = pygame.transform.flip(sprite_base, self.direcao == "esquerda", False)

            if self.timer_estado <= 0:
                self.estado = 'pulo'
                self.velocidade_y = -48 
                self.subindo = True
                


        elif self.estado == 'pulo':
            self.rect.y += self.velocidade_y
            self.velocidade_y += 0.9
            
            # Define se o sprite está subindo ou descendo com base na velocidade_y
            if "subindo" in recursos.sprites_boss_pulo and "caindo" in recursos.sprites_boss_pulo:
                if self.velocidade_y < 0:
                    sprite_base = recursos.sprites_boss_pulo["subindo"]
                else:
                    sprite_base = recursos.sprites_boss_pulo["caindo"]
                self.sprite_atual = pygame.transform.flip(sprite_base, self.direcao == "esquerda", False)

            if self.velocidade_y < 15:
                if self.rect.centerx < jogador_rect.centerx:
                    self.rect.x += 24 
                    self.direcao = "direita"
                else:
                    self.rect.x -= 24
                    self.direcao = "esquerda"
            
            # Se tocou o chão de volta
            if self.rect.bottom >= config.chao.y:
                self.rect.bottom = config.chao.y
                self.estado = 'vulneravel_pos_pulo' # Mudamos temporariamente o estado para mostrar o pouso
                self.timer_estado = 15 # Tempo que ele fica "achatado" no chão descansando do impacto



        elif self.estado == 'vulneravel_pos_pulo':
            self.timer_estado -= 1
            
            # Sprite dele impactado no chão
            if "pouso" in recursos.sprites_boss_pulo:
                sprite_base = recursos.sprites_boss_pulo["pouso"]
                self.sprite_atual = pygame.transform.flip(sprite_base, self.direcao == "esquerda", False)
                
            if self.timer_estado <= 0:
                self.estado = 'descanso'
                self.timer_estado = 60 # Volta pro descanso normal



        elif self.estado == 'ataque_chao':
            self.timer_estado -= 1
            
            # No primeiro frame da preparação, spawna o trampolim 
            if not self.trampolim_ativo:
                self.trampolim_ativo = True
                offset_x = random.choice([-300, 300]) 
                posicao_trampolim_x = jogador_rect.centerx + offset_x
                posicao_trampolim_x = max(100, min(posicao_trampolim_x, 1820)) 
                
                self.rect_trampolim = pygame.Rect(posicao_trampolim_x, config.chao.y - 40, 120, 40)

            # Sprite de preparação
            if self.timer_estado > 0 and "prepara" in recursos.sprites_boss_investida:
                sprite_base = recursos.sprites_boss_investida["prepara"]
                self.sprite_atual = pygame.transform.flip(sprite_base, self.direcao == "esquerda", False)

            # Execução do Dash após a preparação acabar
            if self.timer_estado <= 0: 
                if self.alvo_x == 0: 
                    self.alvo_x = -20 if self.rect.centerx > jogador_rect.centerx else 20 
                    # Define a direção olhando para o lado do movimento
                    self.direcao = "esquerda" if self.alvo_x < 0 else "direita"
                
                # Sprite dele deslizando durante o dash
                if "dash" in recursos.sprites_boss_investida:
                    sprite_base = recursos.sprites_boss_investida["dash"]
                    self.sprite_atual = pygame.transform.flip(sprite_base, self.direcao == "esquerda", False)

                self.rect.x += self.alvo_x 
                
                if self.rect.left <= 0 or self.rect.right >= 1920: 
                    self.rect.left = max(0, min(self.rect.left, 1920 - self.rect.width)) 
                    self.estado = 'descanso' 
                    self.timer_estado = 60 
                    self.alvo_x = 0 
                    self.trampolim_ativo = False 


    def desenhar(self, superficie):
        if self.vivo:
            if self.rect is None or not isinstance(self.rect, pygame.Rect): 
                posicao_desenho = pygame.Rect(1500, config.chao.y - 400, 300, 400) 
            else:
                posicao_desenho = self.rect 

            if self.sprite_atual: 
                superficie.blit(self.sprite_atual, posicao_desenho.topleft)
            else:
                pygame.draw.rect(superficie, self.cor, posicao_desenho) 

        # Desenha trampolim se ele estiver ativo
        if self.trampolim_ativo and recursos.sprite_trampolim:
            superficie.blit(recursos.sprite_trampolim, self.rect_trampolim.topleft)