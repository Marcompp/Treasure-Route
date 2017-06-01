import pygame, sys
import Classes as CT
from random import randint
pygame.init()
check = 0
contador = 0
largura,altura = 640,480
#clr1=(22,122,211)
#clr2=(255,44,166)
#clr3=(34,55,245)
screen = pygame.display.set_mode((largura,altura),0,32)
i = 0
#Quantas vezes o programa roda por segundo
clock = pygame.time.Clock()
barco = pygame.image.load("Barco.png")
Mar_img = pygame.image.load("mar.png")
nuvem = pygame.image.load("nuvem.png")
Sol = pygame.image.load("Sol.png")
Sol = pygame.transform.scale(Sol,(160,140))
Lista_Nuvem = []

conta = 0

FPS = 30

while True:
    CT.sair()
    

    screen.fill((20,160,200))
    
    
    #pygame.draw.line(screen, clr2, (0,0),(640,360),5)
    #pygame.draw.rect(screen,clr3,(40,40,300,45))
    #pygame.draw.circle(screen,clr1,(350,200),80,40)
    
    
    contador = CT.Mar(barco,Mar_img,contador,screen,largura,altura,Sol)
    
    CT.Nuvem_spawn(nuvem,Lista_Nuvem,largura,150,conta,screen,0.5,100,300,10000)
    
    
        

    
    pygame.display.flip()
    
    clock.tick(FPS)