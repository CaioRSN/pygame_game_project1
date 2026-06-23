<<<<<<< HEAD
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
        
        self.plataformas_flutuantes = list(self.plataformas_originais)
        self.blocos_cenario = list(self.blocos_originais)
        
        import copy
        self.inimigos = copy.deepcopy(self.inimigos_originais)
=======
import config

class Cenario:
    def __init__(self, indice_fundo, plataformas, blocos):
        self.indice_fundo = indice_fundo
        self.plataformas_flutuantes = plataformas
        self.blocos_cenario = blocos

    def carregar(self):
        config.indice_fundo = self.indice_fundo
        config.plataformas_flutuantes = self.plataformas_flutuantes
        config.blocos_cenario = self.blocos_cenario
>>>>>>> 6bf9d4e27b6ccccba47567619f2bc691bfc7553b
