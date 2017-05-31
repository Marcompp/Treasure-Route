import pygame
from pygame.locals import *
import Evento
from sys import exit
import time
import random
import Batalha
import Misc
import json


randevs=["Newspaper","TrainSkl","Castaway","Magicbo","Rowboat"]
foodevs=["Eatfood","Eatfood","Eatfood","Feast","Alcoffering"]
ratievs=["Rationfood","Foodfight"]
hungevs=["Cannibal","Starving"]
despevs=["Suicide"]
locaevs=["Carthusport","BrigandIsles"]

#fonte
pygame.init()

pygame.font.init()
font_name = pygame.font.get_default_font()
game_font = pygame.font.Font("Treamd.ttf", 30)


#start pygame
screen = pygame.display.set_mode((640, 480), 0, 32)


background_filename = 'Mar proto.png'
background = pygame.image.load(background_filename).convert()

goal_filename = "Goal.png"
goal = pygame.image.load(goal_filename).convert_alpha()

ind_filename = "Indic.png"
indicator = pygame.image.load(ind_filename).convert_alpha()

paper = pygame.image.load('paper2.png').convert()

pygame.display.set_caption('Pyga')
clock = pygame.time.Clock()


phase = 0
timeod = 0
progress = 0
nexev = 0
while True:
	ship = Misc.Loadship()#{"surface":1,"pos":35,"speed":3,"durability":10}
	party = Misc.Loadparty()
	supply = Misc.Loadsupply()
	pos = Misc.Loadpos()
	story = Misc.Loadstory()
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()
	screen.blit(background, (0, 0))
	#screen.blit(indicator,(ship["pos"],10))
	screen.blit(goal,(465,15))
	#screen.blit(linha, 20,20)
	screen.blit(indicator,(pos,10))

	Batalha.blitcards(screen)
	Batalha.blitsupply(screen)

	if progress == 20:
		pos += ship["speed"]
		progress = 0
	if pos == 460:
		getattr(Evento,Goal)(screen)

	if timeod == 90:
		if supply["food"] >= len(party)*2:
			getattr(Evento,foodevs[random.randrange(len(foodevs))])(screen)
		elif supply["food"] != 0:
			getattr(Evento,ratievs[random.randrange(len(ratievs))])(screen)
		else:
			getattr(Evento,hungevs[random.randrange(len(hungevs))])(screen)
		timeod = 0
	if nexev >=23:
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