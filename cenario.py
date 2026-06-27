import config
import copy
import pygame

class Cenario:
    def __init__(self, indice_fundo, plataformas, blocos, inimigos):
        self.indice_fundo = indice_fundo
        self.plataformas_originais = plataformas
        self.blocos_originais = blocos
        self.inimigos_originais = inimigos
        
        self.plataformas_flutuantes = []
        self.blocos_cenario = []
        self.inimigos = []
        self.carregar()

    def carregar(self):
        config.indice_fundo = self.indice_fundo
        
        # Criamos a lista de dicionários para gerenciar os estados individuais de tempo
        self.plataformas_flutuantes = []
        for p in self.plataformas_originais:
            self.plataformas_flutuantes.append({
                "rect": p[0].copy(),
                "sprite_id": p[1],
                "tempo_parado": 0,           # Contador de frames em cima da plataforma
                "invisivel": False,          # Controla se ela sumiu ou não
                "tempo_invisivel": 0,        # Contador de frames que ela fica invisível
                "original_rect": p[0].copy() # Guarda a coordenada real para quando ela voltar
            })
            
        self.blocos_cenario = list(self.blocos_originais)
        # Faz uma cópia dos inimigos originais para reiniciar o estado deles na fase[cite: 4]
        self.inimigos = copy.deepcopy(self.inimigos_originais)
        
        # Atualiza o arquivo de configuração global
        config.plataformas_flutuantes = self.plataformas_flutuantes
        config.blocos_cenario = self.blocos_cenario
        config.inimigos_cenario = self.inimigos

    def atualizar_plataformas(self, jogador_rect, jogador_pulando):
        """Atualiza os cronômetros das plataformas e retorna os retângulos de colisão ativos."""
        lista_colisoes_ativas = []

        for p in self.plataformas_flutuantes:
            if p["invisivel"]:
                p["tempo_invisivel"] += 1
                # 2 segundos a 60 FPS = 120 frames
                if p["tempo_invisivel"] >= 120:
                    p["invisivel"] = False
                    p["tempo_invisivel"] = 0
                    p["tempo_parado"] = 0
                    p["rect"] = p["original_rect"].copy()  # Restaura a colisão
            else:
                # Cria uma pequena linha de colisão logo acima da plataforma para checar se o pé do jogador está nela
                area_pe = pygame.Rect(p["rect"].x, p["rect"].y - 5, p["rect"].width, 5)
                
                # Se o jogador colidir com o topo e não estiver subindo/pulando
                if jogador_rect.colliderect(area_pe) and not jogador_pulando:
                    p["tempo_parado"] += 1
                    
                    # 5 segundos a 60 FPS = 300 frames
                    if p["tempo_parado"] >= 300:
                        p["invisivel"] = True
                        p["tempo_invisivel"] = 0
                        # Remove a colisão temporariamente jogando o rect para fora do mapa
                        p["rect"] = pygame.Rect(-1000, -1000, 0, 0)
                else:
                    # Se o jogador sair da plataforma, o contador vai diminuindo gradativamente
                    if p["tempo_parado"] > 0:
                        p["tempo_parado"] -= 1

            # Apenas plataformas visíveis mantêm colisão ativa no jogo
            if not p["invisivel"]:
                lista_colisoes_ativas.append(p["rect"])

        # Retorna a soma das colisões das plataformas ativas com os blocos fixos do cenário
        return lista_colisoes_ativas + [b[0] for b in self.blocos_cenario]
