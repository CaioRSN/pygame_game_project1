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