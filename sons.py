import pygame

class Musicas:
    def __init__(self):
        self.tiro = pygame.mixer.Sound("music/Disparo.mp3")
        self.dano = pygame.mixer.Sound("music/dano.mp3")
        self.teclado = pygame.mixer.Sound("music/teclado.mp3")
        self.tela_morte = pygame.mixer.Sound("music/tela de morte.mp3")
        self.click = pygame.mixer.Sound("music/click.mp3")
        self.click.set_volume(0.3)
        self.pulo = pygame.mixer.Sound("music/pulo.mp3")
        self.pulo.set_volume(0.1)
        self.coletar = pygame.mixer.Sound("music/coletar.mp3")
        self.coletar.set_volume(0.5)
        self.monstro = pygame.mixer.Sound("music/monstro.mp3")
        self.mola = pygame.mixer.Sound("music/mola.mp3")
        self.vitoria = pygame.mixer.Sound("music/vitoria.mp3")

    def tocar_tiro(self):
        self.tiro.play()

    def tocar_dano(self):
        self.dano.play()

    def tocar_teclado(self):
        self.teclado.play()

    def tocar_tela_morte(self):
        self.tela_morte.play()

    def tocar_click(self):
        self.click.play()

    def tocar_pulo(self):
        self.pulo.play()

    def tocar_coleta(self):
        self.coletar.play()

    def tocar_monstro(self):
        self.monstro.play()

    def tocar_mola(self):
        self.mola.play()

    def tocar_vitoria(self):
        self.vitoria.play()

    def tocar_musica_fundo(self):
        pygame.mixer.music.load("music/musica_fundo.mp3")
        pygame.mixer.music.set_volume(0.1)
        pygame.mixer.music.play(-1)

    def parar_musica_fundo(self):
        pygame.mixer.music.stop()