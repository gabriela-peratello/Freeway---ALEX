import pygame as gp

#CRIAR A CLASSE JOGADOR
 
class Jogador:
    def __init__(self, local_imagem, largura, altura, inix, iniy, local_som): 
        self.imagem = gp.image.load(local_imagem) #onde a imagem ta
        self.imagem = gp.transform.scale(self.imagem,(largura, altura)) #define a largura e altura
        self.mask = gp.mask.from_surface(self.imagem ) #MASCARA

        #POSIÇÃO INICIAL X E Y
        self.iniy = iniy #ini = posição inicial
        self.inix = inix

        self.px = self.inix #px = posição
        self.py = self.iniy

        self.largura = largura
        self.altura = altura

        #PONTOS
        self.pontuacao = 0

        #VELOCIDADE
        self.velocidade = 5

        #EFEITO SONORO
        self.som = gp.mixer.Sound(local_som)
        
    def movimento (self, direita, esquerda):
            teclas = gp.key.get_pressed() #lista as teclas apertadas
            if teclas[direita]:
                if self.px < (1920 - self.largura):
                    self.px += 4
            if teclas[esquerda]:
                if self.px > 0:
                    self.px -= 4
            
            