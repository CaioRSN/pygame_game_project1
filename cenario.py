import config
import copy

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
        
        self.plataformas_flutuantes = list(self.plataformas_originais)
        self.blocos_cenario = list(self.blocos_originais)
        
        # Faz uma cópia dos inimigos originais para reiniciar o estado deles na fase
        self.inimigos = copy.deepcopy(self.inimigos_originais)
        
        # Atualiza o arquivo de configuração global
        config.plataformas_flutuantes = self.plataformas_flutuantes
        config.blocos_cenario = self.blocos_cenario
        config.inimigos_cenario = self.inimigos
