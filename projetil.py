import pygame
import config

class Projetil(pygame.sprite.Sprite):
    def __init__(self, x, y, direcao):
        super().__init__()
        
        # Define o lado do tiro e a sprite usada
        self.direcao = direcao
        self.tipo_sprite = config.indice_sprite_projetil
        
        # Cria a caixa de colisão do tiro
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocidade = 10

    def atualizar(self):
        # Move o projétil sozinho baseado na direção
        self.rect.x += 12 * self.direcao
        
        # Retorna True se o tiro saiu do mapa para saber quando apagar
        if self.rect.x < 0 or self.rect.x > 1920:
            return True
        return False