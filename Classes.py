import pygame,sys
from random import randint


def Mar(barco,Mar_img,contador,screen,largura,altura,Sol):
    h = -40
    contador+=3.5
    if contador<30:
        
        while h != 200:
            screen.blit(Mar_img,(0,h))
            h+=  30
        screen.blit(barco,(largura/8-100,altura/8-40))
        
       
        
    else:
        while h != 200:
            screen.blit(Mar_img,(-40,h))
            h+=  30
        screen.blit(barco,(largura/8-100,altura/8-30))
        
        if contador >= 60:
            contador = 0
    return contador

def sair():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
def Nuvem_spawn(nuvem,Lista_Nuvem,largura,ymax,conta,screen,velocidade,tamanho_min,tamanho_max,chance):
        
            
        Nuvem_True = randint(0,chance)
    
    
    
        if Nuvem_True<50:
            tamanho = randint(tamanho_min,tamanho_max)
            y = randint(-40,ymax)
            x = largura
        
            coisa = pygame.transform.scale(nuvem,(tamanho,tamanho))
            
            NUVEM = {"imagem":coisa,
                 "y": y,
                 "x": x,
                 "tamanho":tamanho}
            
            Lista_Nuvem.append(NUVEM)
        while conta <= len(Lista_Nuvem)-1:
            Lista_Nuvem[conta]["x"] -=velocidade
        
            if Lista_Nuvem[conta]["x"] <= -Lista_Nuvem[conta]["tamanho"]:
            
                Lista_Nuvem.remove(Lista_Nuvem[conta])
                

            else:   
                screen.blit(Lista_Nuvem[conta]["imagem"],(Lista_Nuvem[conta]["x"],Lista_Nuvem[conta]["y"]))
                conta +=1