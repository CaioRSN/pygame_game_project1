import config
import copy
import pygame

class Cenario:
    def __init__(self, indice_fundo, plataformas, blocos, inimigos):
        self.indice_fundo = indice_fundo
        self.plataformas_originais = plataformas
        self.blocos_originais = blocos
        self.inimigos_originais = inimigos
        
        # Variáveis dinâmicas da fase
        self.plataformas_flutuantes = []
        self.blocos_cenario = []
        self.inimigos = []
        
        self.carregar()

    def carregar(self):
        # Reinicia o estado global
        config.indice_fundo = self.indice_fundo
        
        # Reseta a flag de crachás gerados para esta fase
        config.crachas_gerados_na_fase = False
        
        # Cria a lista de dicionários para gerenciar as plataformas temporizadas
        self.plataformas_flutuantes = []
        for p in self.plataformas_originais:
            self.plataformas_flutuantes.append({
                "rect": p[0].copy(),
                "sprite_id": p[1],
                "tempo_parado": 0,    # Contador de frames com o jogador em cima
                "invisivel": False,   # Controla se a plataforma está ativa ou não
                "tempo_invisivel": 0, # Contador de frames que ela fica invisível
                "original_rect": p[0].copy() # Guarda a coordenada real para quando ela voltar
            })
            
        self.blocos_cenario = list(self.blocos_originais)
        
        # Faz uma cópia profunda para reiniciar o estado de vida dos inimigos
        self.inimigos = copy.deepcopy(self.inimigos_originais)
        
        # Atualiza o arquivo de configuração global com os novos objetos da fase
        config.plataformas_flutuantes = self.plataformas_flutuantes
        config.blocos_cenario = self.blocos_cenario
        config.inimigos_cenario = self.inimigos

    def spawnar_crachas(self, img_cracha):
        if not self.plataformas_flutuantes:
            return # Não há plataformas para spawnar

        menor_y = min(p["rect"].y for p in self.plataformas_flutuantes)

        # Filtra todas as plataformas que compartilham desse menor Y
        plataformas_mais_altas = [p for p in self.plataformas_flutuantes if p["rect"].y == menor_y]

        # Cria um coletável para cada plataforma encontrada nessa altura máxima
        for plat in plataformas_mais_altas:
            rect_plat = plat["rect"]
            x_item = rect_plat.x + (rect_plat.width // 2) - 27 
            y_item = rect_plat.y - 65 

            config.itens_no_chao.append({
                "tipo": "cracha",
                "rect": pygame.Rect(x_item, y_item, 55, 55), 
                "imagem": img_cracha
            })
        # função que atualiza as colisões
    def atualizar_plataformas(self, jogador_rect, jogador_pulando):
        lista_colisoes_ativas = []
        
        for p in self.plataformas_flutuantes:
            if p["invisivel"]:
                p["tempo_invisivel"] += 1
                
                if p["tempo_invisivel"] >= 120:
                    p["invisivel"] = False
                    p["tempo_invisivel"] = 0
                    p["tempo_parado"] = 0
                    p["rect"] = p["original_rect"].copy() # Restaura a colisão
                    
            else:
                # Cria uma pequena linha de colisão logo acima da plataforma para checar o pé do jogador
                area_pe = pygame.Rect(p["rect"].x, p["rect"].y - 5, p["rect"].width, 5)
                
                # Se o jogador colidir com o topo e não estiver subindo/pulando
                if jogador_rect.colliderect(area_pe) and not jogador_pulando:
                    p["tempo_parado"] += 1
                    if p["tempo_parado"] >= 120: 
                        p["invisivel"] = True
                        p["tempo_invisivel"] = 0
                        # Remove a colisão temporariamente movendo o rect para fora do mapa
                        p["rect"] = pygame.Rect(-1000, -1000, 0, 0)
                else:
                    # Se o jogador sair da plataforma, o contador vai diminuindo gradativamente
                    if p["tempo_parado"] > 0:
                        p["tempo_parado"] -= 1
            
            # Apenas plataformas visíveis mantêm colisão ativa no jogo
            if not p["invisivel"]:
                lista_colisoes_ativas.append(p["rect"])
                
        # Retorna a soma das colisões das plataformas flutuantes ativas com os blocos fixos do cenário
        return lista_colisoes_ativas + [b[0] for b in self.blocos_cenario]
