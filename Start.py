import pygame
from pygame.locals import *
import Evento
from sys import exit
import time
import random
import Batalha
import Misc
import json
import Menu
import Classes as CT

randevs=["Newspaper","TrainSkl","TrainStr","TrainInt","Castaway","Magicbo","Rowboat","Fishday"]
foodevs=["Eatfood","Eatfood","Eatsup","Feast","Alcoffering"]
ratievs=["Rationfood","Foodfight"]
hungevs=["Cannibal","Starving"]
despevs=["Suicide","Pullweight"]
locaevs=["Carthusport","BrigandIsles"]

#fonte
pygame.init()

pygame.font.init()
font_name = pygame.font.get_default_font()
game_font = pygame.font.Font("Treamd.ttf", 30)

pygame.mixer.init()

def barco():
	ship = Misc.Loadship()
	image= pygame.image.load(ship["surface"]).convert_alpha()
	return pygame.transform.rotate(image,10)

def Gameover(screen):
	Text = ["No one survived to claim Howell",
			"D'Or's treasure. Too bad."]
	y = Evento.walloftext(Text,screen)
	Evento.proceed(screen)

#start pygame
screen = pygame.display.set_mode((640, 480), 0, 32)

Nuvem_filename = 'Nuvem.png'
Nuvem = pygame.image.load(Nuvem_filename).convert_alpha()

Sol_filename = 'Sol.png'
Sol = pygame.image.load(Sol_filename).convert_alpha()
Sol = pygame.transform.scale(Sol,(140,120))

mar_filename = 'mar.png'
mar = pygame.image.load(mar_filename).convert_alpha()

goal_filename = "Goal.png"
goal = pygame.image.load(goal_filename).convert_alpha()

ind_filename = "Indic.png"
indicator = pygame.image.load(ind_filename).convert_alpha()

paper = pygame.image.load('paper2.png').convert()

pygame.display.set_caption('Treasure Route')
clock = pygame.time.Clock()

CT.Mudar_musica("Calm.ogg")
while True:
	Evento.endar()
	select = Menu.mainmenu(screen)
	if select == 2:
		Menu.newgame(screen)
		select = 1
	if select == 1:
		try:
			ship = Misc.Loadship()#{"surface":1,"pos":35,"speed":3,"durability":10}
			party = Misc.Loadparty()
			supply = Misc.Loadsupply()
			pos = Misc.Loadpos()
			story = Misc.Loadstory()
		except ValueError:
			Menu.newgame(screen)
		Lista_Nuvem = [{"imagem":Nuvem,"y": 0,"x": -120,"tamanho":300},{"imagem":Nuvem,"y": 30,"x": 200,"tamanho":300},{"imagem":Nuvem,"y": 5,"x": 440,"tamanho":300}]
		contador =0
		conta = 0
		phase = 0
		timeod = 0
		progress = 0
		nexev = 0
		if "GameO" in story:
			Menu.newgame(screen)

		CT.Mudar_musica("musicapiratas.ogg")
		while "GameO" not in story:
			ship = Misc.Loadship()#{"surface":1,"pos":35,"speed":3,"durability":10}
			party = Misc.Loadparty()
			supply = Misc.Loadsupply()
			pos = Misc.Loadpos()
			story = Misc.Loadstory()
			for event in pygame.event.get():
				if event.type == QUIT:
					exit()

			screen.fill((20,160,200))

			w,h = pygame.display.get_surface().get_size()
			
			screen.blit(Sol,(w-250,50))
			CT.Nuvem_spawn(Nuvem,Lista_Nuvem,w,20,conta,screen,2.5,100,300,5000)

			contador = CT.Mar(barco(),mar,contador,screen,w,h,Sol)

			#screen.blit(indicator,(ship["pos"],10))
			screen.blit(goal,(465,15))
			for x in range (1, 17):
				pygame.draw.line(screen,(255,0,0),(x*28,26),(x*28+20,26),3)
			#screen.blit(linha, 20,20)
			screen.blit(indicator,(pos,10))

			Batalha.blitcards(screen)
			Batalha.blitsupply(screen)

			wait = 3

			if party == []:
				Gameover(screen)
				select = 0
				story.append("GameO")
				Misc.Savestory(story)
				break

			if progress == 20*wait:
				pos += ship["speed"]
				progress = 0
			if pos >= 0 and "NG" not in story:
			#	getattr(Evento,"Battletest")(screen)
				Evento.Newgame(screen)
				story.append("NG")
				Misc.Savestory(story)
			elif pos >= 460:
				getattr(Evento,"Goal")(screen)
				story.append("GameO")
				Misc.Savestory(story)
				break

			elif timeod >= 90*wait:
				if supply["food"] >= len(party)*2:
					getattr(Evento,foodevs[random.randrange(len(foodevs))])(screen)
				elif supply["food"] != 0:
					getattr(Evento,ratievs[random.randrange(len(ratievs))])(screen)
				else:
					getattr(Evento,hungevs[random.randrange(len(hungevs))])(screen)
				timeod = 0
			elif nexev >=24*wait:
				x = random.randrange(1,9)
				if x >= 5:
					y = random.randrange(len(party))
					if party[y]["mor"]<= 0:
						getattr(Evento,despevs[random.randrange(len(despevs))])(y ,screen)
					else:
						getattr(Evento,randevs[random.randrange(len(randevs))])(screen)
					nexev =0
			progress+= 1
			nexev += 1
			timeod +=1
			Misc.Savepos(pos)
			
			#Misc.Save(party,supply,ship,pos,story)
			pygame.display.update()
			time_passed = clock.tick(30)
		CT.Mudar_musica("Calm.ogg")
	if select ==3:
		Text=["Programming, writing and design - Marco",
			"Programing and graphics design - Juliano",
			"Sound design - Leonardo",
			"",
			"Special Thanks: Luciano, Camila"]
		Evento.walloftext(Text,screen)
		Evento.proceed(screen)
