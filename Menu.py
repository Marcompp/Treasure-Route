import pygame
from pygame.locals import *
import Evento
from sys import exit
import time
import random
import Batalha
import Misc
import json


pygame.init()

letter = 40

pygame.font.init()
font_name = pygame.font.get_default_font()
game_font = pygame.font.Font("Treamd.ttf", letter)

def telatitulo():
	dimensao = (640, 480)
	imagem = pygame.image.load('initground.png').convert()
	imagem = pygame.transform.scale(imagem,dimensao)
	return imagem

def arrow():
	return pygame.image.load('indic2.png').convert_alpha()

def endar():
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

def mainmenu(screen):
	lag =0
	cursor = 1
	clock = pygame.time.Clock()
	while True:
		endar()
		posx = 40
		screen.blit(telatitulo(),(0,0))
		posy = 215
		options = ["Continue","New Game","Credits"]
		y =0
		for tex in options:
			tex1 = game_font.render(tex, 1, (0, 0, 0))
			screen.blit(tex1, (posx,posy+y))
			y += letter

		pressed_keys = pygame.key.get_pressed()
		if lag >=5:
			if pressed_keys[K_UP]:
				cursor -=1
				lag = 0
			elif pressed_keys[K_DOWN]:
				cursor +=1
				lag = 0
			elif pressed_keys[K_LEFT]:
				cursor -=1
				lag = 0
			elif pressed_keys[K_RIGHT]:
				cursor +=1
				lag = 0
			elif pressed_keys[K_SPACE]:
				return cursor
		if cursor > len(options):
			cursor = len(options)
		if cursor <=0:
			cursor = 1
		if cursor == 1:
			screen.blit(arrow(), (posx-15,posy-5))
		elif cursor == 2:
			screen.blit(arrow(), (posx-15,posy-5+letter))
		elif cursor == 3:
			screen.blit(arrow(), (posx-15,posy-5 + letter*2))
		lag+=1
		pygame.display.update()
		time_passed = clock.tick(30)
	
def newgame(screen):
	char = Misc.Charlist()
	supply = {"food": 20, "arrows": 0, "potions": 10, "gold": 5}
	boat = {"surface": 1, "pos": 335, "speed": 3, "durability": 10}
	pos = 20
	Misc.Save([char["Mayara"],char["Juju"]],supply,boat,pos,["Mayara","Juju"])