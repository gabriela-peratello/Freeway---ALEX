import pygame as gp
import random 


class Inimigos:
    def __init__(self, local_imagem, lar, alt ):
        #TAMANHO DO INIMIGO 
        self.lar = lar
        self.alt = alt

        #ARRUMANDO AS IMAGENS
        self.imagem = gp.image.load(local_imagem) 
        self.imagem = gp.transform.scale(self.imagem,(self.lar, self.alt)) #TRANSFORMAR O TAMANHO 
        self.mask = gp.mask.from_surface(self.imagem ) #MASCARA

        self.inx = random.choice([200, 400, 600, 800, 1000, 1200, 1400, 1800])
        self.iny = -300 

        #POSIÇÃO INIMIGOS 
        self.px = self.inx
        self.py = self.iny
       
       #DEFINIR DE ONDE OS MORTYS CAIEM
        self.linha = [ 200, 600, 1000, 1400, ] 
        self.px = random.choice(self.linha)
        
        #VELOCIDADE
        self.velocidade = random.randint(1,5) 

    #DESENHA OS MORTYS
    def desenho_morty(self, tela):
        tela.blit(self.imagem,(self.px,self.py)) #POSIÇÕES 

    #MOVIMENTA OS MORTYS
    def movimento_morty(self): 
        self.py += self.velocidade
        if self.py > 1000:
            self.py = self.iny
            self.velocidade = random.randint(1,5)
            self.px = random.choice(self.linha)