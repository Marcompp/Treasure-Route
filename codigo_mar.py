import pygame, sys


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
Nuvem = pygame.image.load("nuvem.png")



FPS = 30

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    i += 5
    if i > 255:
       i = 0
    screen.fill((0,200,255))
    
    #pygame.draw.line(screen, clr2, (0,0),(640,360),5)
    #pygame.draw.rect(screen,clr3,(40,40,300,45))
    #pygame.draw.circle(screen,clr1,(350,200),80,40)
    
    
    screen.blit(Nuvem,(100,50))
    
    h = -40
    contador+=1
    if contador<30:
        
        while h != 200:
            screen.blit(Mar_img,(0,h))
            h+=  30
        screen.blit(barco,(largura/8,altura/8+30))
       
        
    else:
        while h != 200:
            screen.blit(Mar_img,(-40,h))
            h+=  30
        screen.blit(barco,(largura/8,altura/8+40))
        if contador == 60:
            contador = 0
  
    
    pygame.display.flip()
    
    clock.tick(FPS)