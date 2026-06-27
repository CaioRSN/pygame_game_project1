import pygame
import config
import recursos

class Jogador(pygame.sprite.Sprite):
    def __init__(self, largura_calculada):
        super().__init__()
        
        self.rect = pygame.Rect(config.POS_X_INICIAL, config.POS_Y_INICIAL, largura_calculada, config.ALTURA_PERSONAGEM)
        
        self.vida_maxima = 5
        self.vida_atual = 5
        
        self.em_hit = False
        self.tempo_hit = 0
        self.direcao_hit = 0
        self.invulneravel = 0
        
        self.pulando = False
        self.velocidade_y = 0
        self.atacando = False
        self.movendo = False

    def gerenciar_movimento(self, teclas):
        if self.em_hit and self.tempo_hit > 30:
            self.rect.x += 6 * self.direcao_hit
            self.movendo = False
            return

        # SE ESTIVER ATACANDO NO CHÃO, TRAVA O MOVIMENTO IMEDIATAMENTE
        if config.atacando and not self.pulando:
            self.movendo = False
            return

        velocidade_x = 0
        andando_direita = False
        andando_esquerda = False

        if teclas[pygame.K_d]:
            velocidade_x += config.velocidade_jogador
            andando_direita = True

        if teclas[pygame.K_a]:
            velocidade_x -= config.velocidade_jogador
            andando_esquerda = True

        self.rect.x += velocidade_x

        if andando_direita or andando_esquerda:
            self.movendo = True
            
            if andando_direita and not andando_esquerda:
                config.direcao = "direita"
            elif andando_esquerda and not andando_direita:
                config.direcao = "esquerda"
        else:
            self.movendo = False

    def aplicar_gravidade_e_colisao(self):
        self.velocidade_y += config.gravidade
        self.rect.y += self.velocidade_y

        if self.rect.colliderect(config.chao) and self.velocidade_y >= 0:
            self.rect.bottom = config.chao.top
            self.velocidade_y = 0
            self.pulando = False 

        for lista_plat in config.plataformas_flutuantes:
            if lista_plat["invisivel"]: 
                continue
            rect_colisao = lista_plat["rect"]
            if self.rect.colliderect(rect_colisao) and self.velocidade_y >= 0:
                if self.rect.bottom <= rect_colisao.top + self.velocidade_y + 1:
                    self.rect.bottom = rect_colisao.top
                    self.velocidade_y = 0
                    self.pulando = False

        for lista_bloco in config.blocos_cenario:
            rect_colisao = lista_bloco[0]
            if self.rect.colliderect(rect_colisao) and self.velocidade_y >= 0:
                if self.rect.bottom <= rect_colisao.top + self.velocidade_y + 1:
                    self.rect.bottom = rect_colisao.top
                    self.velocidade_y = 0
                    self.pulando = False

    def atualizar_estados(self):
        if self.em_hit:
            self.tempo_hit -= 1
            if self.tempo_hit <= 0:
                self.em_hit = False 
                
        if self.invulneravel > 0:
            self.invulneravel -= 1

    def desenhar(self, tela, sprite_mostrar):
        if sprite_mostrar is None:
            return
            
        pos_x_centralizado = self.rect.centerx - (sprite_mostrar.get_width() // 2)

        if self.invulneravel > 0 and (self.invulneravel // 4) % 2 == 0:
            return

        tela.blit(sprite_mostrar, (pos_x_centralizado, self.rect.y))
    
    def atualizar_tiro(self, teclas, tempo_atual):
        from projetil import Projetil
        if teclas[pygame.K_k] and not self.em_hit:
            config.atacando = True  
            if not self.pulando:
                self.movendo = False
                
            if tempo_atual - config.ultimo_disparo > config.cooldown_disparo:
                pos_x = self.rect.right if config.direcao == "direita" else self.rect.left - 30
                pos_y_ajustado = self.rect.centery - 30 
                direcao_tiro = 1 if config.direcao == "direita" else -1
                
                config.projeteis.append(Projetil(pos_x, pos_y_ajustado, direcao_tiro))
                config.indice_sprite_projetil = 1 - config.indice_sprite_projetil
                config.ultimo_disparo = tempo_atual
        else:
            config.atacando = False

    def receber_dano(self, pinguim):
        if self.rect.colliderect(pinguim.rect) or pinguim.atacando:
            if self.rect.colliderect(pinguim.rect) and self.invulneravel <= 0:
                self.vida_atual -= 1
                self.em_hit = True
                self.tempo_hit = 48  
                self.invulneravel = 75 
                config.frame_atual = 0.0      
                config.tempo_descanso_inimigo = 60
                
                # Ajusta perfeitamente a direção do empurrão baseado de onde veio o inimigo
                if pinguim.rect.x < self.rect.x:
                    self.direcao_hit = 1  
                else:
                    self.direcao_hit = -1
                    
                if self.vida_atual <= 0:
                    self.vida_atual = 0
                    return True
        return False

    def atualizar_animacao(self):
        import recursos
        if self.em_hit:
            var_lista_atual = recursos.sprites_personagem_pos_hit
            velocidade_anim_atual = 0.13
        elif config.atacando:
            var_lista_atual = recursos.sprites_atacando
            velocidade_anim_atual = 0.15 
        elif self.pulando:
            config.frame_atual = 0 
            if self.velocidade_y < -5:
                personagem_sprite = recursos.sprite_prepara_pulo
            elif -5 <= self.velocidade_y <= 5:
                personagem_sprite = recursos.sprite_no_ar
            else:
                personagem_sprite = recursos.sprite_caindo
            return pygame.transform.flip(personagem_sprite, True, False) if config.direcao == "esquerda" else personagem_sprite
        else:
            if self.movendo:
                var_lista_atual = recursos.sprites_correndo
                velocidade_anim_atual = 0.25 
            else:
                var_lista_atual = recursos.sprites_parado
                velocidade_anim_atual = 0.02

        config.frame_atual += velocidade_anim_atual
        if config.frame_atual >= len(var_lista_atual):
            config.frame_atual = 0
        personagem_sprite = var_lista_atual[int(config.frame_atual)]

        if config.direcao == "esquerda":
            return pygame.transform.flip(personagem_sprite, True, False)
        return personagem_sprite
