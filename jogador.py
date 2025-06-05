import pygame as gp

#CRIAR A CLASSE JOGADOR
 
class Jogador:
    def __init__(self, local_imagem, largura, altura, inix, iniy): 
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
        


    def movimento (self, direita, esquerda,baixo,cima):
            teclas = gp.key.get_pressed() #lista as teclas apertadas
            if teclas[direita]:
                if self.px < (1920 - self.largura):
                    self.px += 4
            if teclas[esquerda]:
                if self.px > 0:
                    self.px -= 4
            if teclas[cima]:
                if self.py > 590:
                    self.py -= 4
            if teclas[baixo]:
                if self.py < (1000 - self.altura):
                    self.py += 4
            