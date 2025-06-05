import pygame as gp
import time
import random
from jogador import Jogador
from inimigo import Inimigos
from bonus import Bonus

#FUNÇÃO PARA TRANSIÇÃO
def fade_out_in(tela, imagem_fundo, cor=(0, 0, 0)):
    fade = gp.Surface((1920, 1000))
    fade.fill(cor)
    for alpha in range(0, 255, 15):
        tela.blit(imagem_fundo, (0, 0))  # ← Redesenha o fundo antes de aplicar o fade
        fade.set_alpha(alpha)
        tela.blit(fade, (0, 0))
        gp.display.update()
        gp.time.delay(12)

#Iniciar
gp.init()
timer = gp.time.Clock() 

#CRIAÇÃO DA TELA
tela = gp.display.set_mode((1920,1000)) #tela + medida

#CRIAÇÃO MUSICA
gp.mixer.music.load("sons/mtema.mp3") 
gp.mixer.music.set_endevent(gp.USEREVENT) #repetição som de fundo
gp.mixer.music.play() #inicia a reprodução


#TELA INICIAL
menu = gp.image.load("fundo/pagini.png") #tras imagem
menu = gp.transform.scale(menu, (1920,1000)) #transforma

#TELA DE TUTORIAL
tutorial = gp.image.load("fundo/tuto2.png")
tutorial = gp.transform.scale(tutorial,(1920,1000))

#TELA PRINCIPAL (CENÁRIO)
cenario = gp.image.load("fundo/garagem.png")
cenario = gp.transform.scale(cenario,(1920,1000)) 

#TELA GAME OVER
perdeu = gp.image.load("fundo/perdeu3.png")
perdeu = gp.transform.scale(perdeu, (1920,1033))

#PONTUAÇÃO NA TELA
pontos = gp.font.SysFont("Bahnschrift", 45, True, False)

#PERSONAGEM
rick = Jogador("Ricks/rick.png",250,250,0,800)

#MORTYS INIMIGOS
lista_mortys = [Inimigos("Mortys/esquisito.png",150,150),
                Inimigos("Mortys/gato.png",200,200),
                Inimigos("Mortys/cartola.png",200,200),
                Inimigos("Mortys/coitadinho.png",200,200)]

#ITENS BONUS
lista_bonus = [Bonus("Ricks/picles.png",200,200),
               Bonus("Ricks/arma.png",200,200),
               Bonus("Ricks/portal.png",200,200)]

#estado e outros
estado = "inicio"
poder_ativo = False
tempo_ativado = 0


#CONTROLAR A JANELA
fj = False

while not fj:
    for evento in gp.event.get(): 
        if evento.type == gp.QUIT: #quit = sair
          fj = True

    if estado == "inicio":
      tela.blit(menu, (0,0))
      gp.display.update()

      teclas = gp.key.get_pressed() 
      if teclas [gp.K_SPACE]:
         fade_out_in(tela, menu)
         estado = "tutorial"
    
    elif estado == "tutorial":
      tela.blit(tutorial, (0,0))
      gp.display.update()

      teclas = gp.key.get_pressed() 
      if teclas [gp.K_a]:
         fade_out_in(tela, tutorial)
         estado = "jogando"
    
    elif estado == "jogando":
        tela.blit(cenario, (0, 0))
        tela.blit(rick.imagem, (rick.px, rick.py)) #comeca nas posições iniciais
        rick.movimento(gp.K_RIGHT, gp.K_LEFT, gp.K_DOWN, gp.K_UP) #movimentar rick

        
        #PRECISA PERCORRER A LISTA (FOR)
        for morty in lista_mortys:
         morty.movimento_morty()
         morty.desenho_morty(tela) #DESENHA OS MORTYS

         if rick.mask.overlap(morty.mask, (morty.px - rick.px, morty.py - rick.py)):
                estado = "FIM"

        for bonus in lista_bonus: #PERCORRE A LISTA BONUS
              bonus.movimento_bonus()
              bonus.desenha_bonus(tela)
              if rick.mask.overlap(bonus.mask, (bonus.px - rick.px, bonus.py - rick.py)):
                rick.pontuacao += 5
                bonus.py = -bonus.alt
                bonus.px = random.randint(0, 1920 - bonus.lar)

        #PODER ESPECIAL        
        teclas = gp.key.get_pressed() 
        if teclas[gp.K_s] and not poder_ativo:
         velocidade = 12
         tempo_ativado = gp.time.get_ticks()  # Tempo atual em milissegundos
         poder_ativo = True

            # Verificar se passou 3 segundos (3000 milissegundos)
        if poder_ativo and gp.time.get_ticks() - tempo_ativado > 3000:
            velocidade = 5
            poder_ativo = False
                
                        

        pontuacao = pontos.render(f"PONTOS:{rick.pontuacao}", True, (139,0,139), (240,255,240)) #fora do for, pq se dentro so aparece qndo encosta
        tela.blit(pontuacao, (0,0))

    elif estado == "FIM":
       tela.blit(perdeu, (0,0))
       pontuacao = pontos.render(f"{rick.pontuacao}", True, (139,0,139), None)
       tela.blit(pontuacao, (960, 650))
       teclas = gp.key.get_pressed()
       if teclas [gp.K_d]:
        time.sleep(0.5)
        estado = "inicio"
        rick.pontuacao = 0  # Zera a pontuação
        rick.velocidade = 5  # Reseta a velocidade
        ativo = False
        gp.mixer.music.play(-1) 
    #COMITAR
   
        
    #ATUALIZAR A TELA
    gp.display.update()
    #VELOCIDADE
    timer.tick(300)