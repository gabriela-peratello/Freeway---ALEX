import pygame as gp
import random

#CRIAR UMA CLASSES PARA OS OBJETOS QUE VALEM PONTO
class Bonus:
    def __init__ (self, local_imagem,lar, alt):
        #TAMANHO
        self.lar = lar
        self.alt = alt

        #ARRUMAR A IMAGENS
        self.imagem = gp.image.load(local_imagem) 
        self.imagem = gp.transform.scale(self.imagem,(self.lar, self.alt)) #TRANSFORMAR O TAMANHO 
        self.mask = gp.mask.from_surface(self.imagem)

        self.inx = 400 #POSIÇÃO INICIAL X 
        self.iny = -200 

        #POSIÇÃO BONUS
        self.px = self.inx
        self.py = self.iny
       
       #DEFINIR DE ONDE OS BONUS CAIEM
        self.linha = [300, 700, 1100, 1700] 
        self.px = random.choice(self.linha)
        
        #VELOCIDADE
        self.velocidade = random.randint(0, 10) 
    
    def desenha_bonus(self, tela):
        tela.blit(self.imagem,(self.px,self.py))

    def movimento_bonus(self):
        self.py += self.velocidade
        if self.py > 1000:
            self.py = self.iny
            self.velocidade = random.randint(0, 10)
            self.px = random.choice(self.linha)