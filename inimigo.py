import pygame
import config
import recursos

class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(1500, config.chao.y - config.ALTURA_PERSONAGEM, 80, config.ALTURA_PERSONAGEM)
        
        # Garante a largura certa se a sprite ja estiver carregada
        if recursos.sprites_pinguin_parado:
            self.rect.width = recursos.sprites_pinguin_parado[0].get_width()
        
        # Variáveis de estado INDIVIDUAIS do inimigo 
        self.vida = 3
        self.vivo = True
        self.movendo = False
        self.atacando = False
        self.frame = 0.0
        self.sprite_atual = None
        self.velocidade = 2.5  
        self.direcao = "esquerda" # Direção própria de cada instância
        
        self.estado = "parado"

    def atualizar_ia(self, jogador_rect):
        if not self.vivo:
            self.sprite_atual = None
            return

        estado_anterior = self.estado

        self.movendo = False
        self.atacando = False

        # Diminui o tempo de descanso a cada frame
        if config.tempo_descanso_inimigo > 0:
            config.tempo_descanso_inimigo -= 1

        # Sempre calcula a distância real para a animação não bugar
        distancia_x = abs(jogador_rect.x - self.rect.x)
        distancia_y = abs(jogador_rect.y - self.rect.y)

        # GATILHO DE ATAQUE: Se estiver perto, ataca
        if distancia_x < 85 and distancia_y < 60:
            self.atacando = True
            self.direcao = "direita" if jogador_rect.x > self.rect.x else "esquerda"
            
        # MODO DESCANSO: Se o jogador se afastar enquanto ele ainda está em cooldown, ele fica parado olhando
        elif config.tempo_descanso_inimigo > 0:
            self.direcao = "direita" if jogador_rect.x > self.rect.x else "esquerda"
            
        # MODO PERSEGUIÇÃO: Se não estiver descansando e estiver no raio de visão, corre atrás
        elif distancia_x < 950 and distancia_y < 200:
            if (jogador_rect.x - self.rect.x) > 15:
                self.rect.x += self.velocidade
                self.direcao = "direita"
                self.movendo = True
            elif (jogador_rect.x - self.rect.x) < -15:
                self.rect.x -= self.velocidade
                self.direcao = "esquerda"
                self.movendo = True

        # Escolhe as locais de animação e define o estado atual
        if self.atacando:
            self.estado = "atacando"
            lista_animacao = recursos.sprites_pinguin_atacando
            velocidade_anim = 0.2
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

class ProjetilInimigo:
    def __init__(self, x, y, direcao):
        self.rect = pygame.Rect(x, y, 20, 10)  # retângulo placeholder
        self.velocidade = 6
        self.direcao = direcao  # "esquerda" ou "direita"

    def atualizar(self):
        if self.direcao == "esquerda":
            self.rect.x -= self.velocidade
        else:
            self.rect.x += self.velocidade


class InimigoDistancia(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(1500, config.chao.y - config.ALTURA_PERSONAGEM, 80, config.ALTURA_PERSONAGEM)

        self.vida = 3
        self.vivo = True
        self.frame = 0.0
        self.sprite_atual = None
        self.direcao = "esquerda"
        self.estado = "parado"
        self.atacando = False
        self.movendo = False

        self.projeteis = []       # lista própria de projéteis
        self.cooldown_tiro = 0
        self.COOLDOWN_MAX = 120   # atira a cada 2 segundos (120 frames)

    def atualizar_ia(self, jogador_rect):
        if not self.vivo:
            self.sprite_atual = None
            return

        distancia_x = abs(jogador_rect.x - self.rect.x)
        distancia_y = abs(jogador_rect.y - self.rect.y)

        # Sempre olha para o jogador
        self.direcao = "direita" if jogador_rect.x > self.rect.x else "esquerda"

        # Decrementa o cooldown a cada frame
        if self.cooldown_tiro > 0:
            self.cooldown_tiro -= 1

        # Se o jogador estiver no alcance, atira
        if distancia_x < 900 and distancia_y < 200:
            self.atacando = True
            if self.cooldown_tiro <= 0:
                proj_x = self.rect.right if self.direcao == "direita" else self.rect.left - 20
                proj_y = self.rect.centery - 5
                self.projeteis.append(ProjetilInimigo(proj_x, proj_y, self.direcao))
                self.cooldown_tiro = self.COOLDOWN_MAX
        else:
            self.atacando = False

        # Atualiza e remove projéteis que saíram da tela
        for proj in self.projeteis[:]:
            proj.atualizar()
            if proj.rect.x > 1920 or proj.rect.x < 0:
                self.projeteis.remove(proj)

        #sprites do pinguim que atira a distancia
        lista_animacao = recursos.sprites_inimigo_distancia_atacando if self.atacando else recursos.sprites_inimigo_distancia_parado
        velocidade_anim = 0.15 if self.atacando else 0.05

        if lista_animacao:
            self.frame += velocidade_anim
            if self.frame >= len(lista_animacao):
                self.frame = 0.0
            sprite_base = lista_animacao[int(self.frame)]
            if self.direcao == "esquerda":
                self.sprite_atual = pygame.transform.flip(sprite_base, True, False)
            else:
                self.sprite_atual = sprite_base