import pygame,sys
from random import randint


def Mar(barco,Mar_img,contador,screen,largura,altura,Sol):
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
    return contador

def sair():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.quit()
                pygame.quit()
                sys.exit()
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            Som("dano.ogg")
        if keys[pygame.K_s]:
            Mudar_musica("musicapiratas.ogg")
        
        
def Nuvem_spawn(nuvem,Lista_Nuvem,largura,ymax,conta,screen,velocidade,tamanho_min,tamanho_max,chance):
        
            
        Nuvem_True = randint(0,chance)
    
    
    
        if Nuvem_True<50:
            tamanho = randint(tamanho_min,tamanho_max)
            y = randint(-10,ymax)
            x = largura
        
            coisa = pygame.transform.scale(nuvem,(tamanho,tamanho))
            
            NUVEM = {"imagem":coisa,
                 "y": y,
                 "x": x,
                 "tamanho":tamanho}
            
            Lista_Nuvem.append(NUVEM)
        for Nuvem in Lista_Nuvem:
            Nuvem["x"] -=velocidade
        
            if Nuvem["x"] <= -Nuvem["tamanho"]:
            
                Lista_Nuvem.remove(Nuvem)
                conta -=1
            else:    
                conta += 1
                screen.blit(Nuvem["imagem"],(Nuvem["x"],Nuvem["y"]))
                
def Mudar_musica(Nova_musica):
    pygame.mixer.quit()
    pygame.mixer.init()
    musica = pygame.mixer.music.load(Nova_musica) 
    pygame.mixer.music.play(-1)              
                
def Som(File_Name):
    som = pygame.mixer.Sound(File_Name)
    pygame.mixer.Sound.play(som)
    