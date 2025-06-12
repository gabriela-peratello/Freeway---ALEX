import pygame as gp
import time
import random
from relativo import caminho_relativo
from jogador import Jogador
from inimigo import Inimigos
from bonus import Bonus



#FUNÇÃO PARA TRANSIÇÃO
def fade_out_in(tela, imagem_fundo, cor=(0, 0, 0)):
    fade = gp.Surface((1920, 1000))
    fade.fill(cor)
    for alpha in range(0, 255, 15):
        tela.blit(imagem_fundo, (0, 0))  #Redesenha o fundo antes de aplicar o fade
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
gp.mixer.music.load(caminho_relativo("sons/mtema.mp3")) 
gp.mixer.music.set_endevent(gp.USEREVENT) #repetição som de fundo
gp.mixer.music.play() #inicia a reprodução

#EFEITOS SONOROS
som_colisao = gp.mixer.Sound(caminho_relativo("sons/tiro.mp3"))
som_bonus = gp.mixer.Sound(caminho_relativo("sons/wubba.mp3"))

#TELA INICIAL
menu = gp.image.load(caminho_relativo("fundo/pagini.png")) #tras imagem
menu = gp.transform.scale(menu, (1920,1000)) #transforma

#TELA DE TUTORIAL
tutorial = gp.image.load(caminho_relativo("fundo/tuto4.png"))
tutorial = gp.transform.scale(tutorial,(1920,1000))

#TELA PRINCIPAL (CENÁRIO)
cenario = gp.image.load(caminho_relativo("fundo/garagem.png"))
cenario = gp.transform.scale(cenario,(1920,1000)) 

#TELA GAME OVER
perdeu = gp.image.load(caminho_relativo("fundo/perdeu3.png"))
perdeu = gp.transform.scale(perdeu, (1920,1033))

#TELA DE VITORIA
ganho = gp.image.load(caminho_relativo("fundo/ganho.png"))
ganho = gp.transform.scale(ganho, (1920,1033))

#PONTUAÇÃO NA TELA
pontos = gp.font.SysFont("Cooper Black", 45, True, False)

#PERSONAGEM
rick = Jogador(caminho_relativo("Ricks/rick.png"),250,250,0,800, caminho_relativo("sons/item.mp3"))

#MORTYS INIMIGOS
lista_mortys = [Inimigos(caminho_relativo("Mortys/esquisito.png"),150,150),
                Inimigos(caminho_relativo("Mortys/gato.png"),200,200),
                Inimigos(caminho_relativo("Mortys/cartola.png"),200,200),
                Inimigos(caminho_relativo("Mortys/coitadinho.png"),200,200)]

#ITENS BONUS
lista_bonus = [Bonus(caminho_relativo("Ricks/picles.png"),200,200),
               Bonus(caminho_relativo("Ricks/arma.png"),200,200),
               Bonus(caminho_relativo("Ricks/portal.png"),200,200)]

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
        rick.movimento(gp.K_RIGHT, gp.K_LEFT) #movimentar rick

        
        #PRECISA PERCORRER A LISTA (FOR)
        for morty in lista_mortys:
         morty.movimento_morty()
         morty.desenho_morty(tela) #DESENHA OS MORTYS
         
         if rick.mask.overlap(morty.mask, (morty.px - rick.px, morty.py - rick.py)):
                som_colisao.play()
                estado = "FIM"

        for bonus in lista_bonus: #PERCORRE A LISTA BONUS
              bonus.movimento_bonus()
              bonus.desenha_bonus(tela)
              if rick.mask.overlap(bonus.mask, (bonus.px - rick.px, bonus.py - rick.py)):
                som_bonus.play()
                rick.pontuacao += 5
                bonus.py = -bonus.alt
                bonus.px = random.randint(0, 1920 - bonus.lar)
        
        pontuacao = pontos.render(f"PONTOS: {rick.pontuacao}", True, (139,0,139), None) #fora do for, pq se dentro so aparece qndo encosta
        tela.blit(pontuacao, (850,50))

    # Poder especial para o Rick
    teclas = gp.key.get_pressed()

    # Ativar o poder (tecla S)
    if teclas[gp.K_s] and not poder_ativo:
        rick.velocidade = 20  # Aumenta a velocidade do Rick (ajuste conforme necessário)
        tempo_ativado = gp.time.get_ticks()  # Marca o tempo que o poder foi ativado
        poder_ativo = True

    # Desativar o poder após 3 segundos
    if poder_ativo and gp.time.get_ticks() - tempo_ativado > 3000:
        rick.velocidade = 5  # Restaura a velocidade normal do Rick
        poder_ativo = False          

    elif estado == "FIM":
       tela.blit(perdeu, (0,0))
       pontuacao = pontos.render(f"{rick.pontuacao}", True, (139,0,139), None)
       tela.blit(pontuacao, (960, 650))

       teclas = gp.key.get_pressed()
       if teclas [gp.K_d]:
        estado = "jogando"
        rick.pontuacao = 0  # Zera a pontuação
        rick.velocidade = 5  # Reseta a velocidade
        rick.px = 0 #reseta posição rick
        rick.py = 800 #reseta posição rick
        ativo = False
        gp.mixer.music.play(-1) 
        for morty in lista_mortys:
                morty.px = random.randint(0, 1920 - morty.lar)
                morty.py = random.randint(-500, -100) # Reaparece acima da tela

        for bonus in lista_bonus:
            bonus.px = random.randint(0, 1920 - bonus.lar)
            bonus.py = random.randint(-800, -300) # Reaparece acima da tela
   
        
    #ATUALIZAR A TELA
    gp.display.update()
    #VELOCIDADE
    timer.tick(300)