import Classes as CT
import pygame,time


def Effects (Sound,Img_String,screen,posx,posy,Width,High):
    
    Imagem = pygame.image.load(Img_String)
    if Width>0 and High>0:
        Imagem = pygame.transform.scale(Imagem,(Width,High))
        
    
    screen.blit(Imagem,(posx,posy))
    pygame.display.flip()
    pygame.mixer.music.set_volume(0.5)
    CT.Som(Sound)
    time.sleep(0.1)
    pygame.mixer.music.set_volume(1)
    
        
    

    