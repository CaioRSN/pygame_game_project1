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