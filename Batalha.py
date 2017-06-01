import pygame
from pygame.locals import *
import Evento
from sys import exit
import time
import random
import Misc
import json

pygame.font.init()
font_name = pygame.font.get_default_font()
game_font = pygame.font.Font("Treamd.ttf", 30)

def supply():
	return pygame.image.load('supply.png').convert()

def arrow():
	return pygame.image.load('Arrow.png').convert()

def fish():
	return pygame.image.load('Fish.png').convert()

def potion():
	return pygame.image.load('Potion.png').convert()

def gold():
	return pygame.image.load('Gold.png').convert()

def card():
	return pygame.image.load('card.png').convert()

def blitcards(screen):
	partyy = Misc.Loadparty()
	x =0
	stats = [["str","skl"],["int","mor"]]
	for chars in partyy:
		screen.blit(card(), (12+x, 351))
		nom = game_font.render(chars["nome"], 1, (0, 0, 0))
		screen.blit(nom, (48+x, 360))
		ph = game_font.render("hp:", 1, (0, 0, 0))
		screen.blit(ph, (52+x, 388))
		if chars["hp"]>=5:
			hpp = game_font.render(str(chars["hp"]), 1, (0, 100, 0))
		else:
			hpp = game_font.render(str(chars["hp"]), 1, (255, 0, 0))
		screen.blit(hpp, (85+x, 388))
		z = 0
		for v in stats:
			y =0
			for a in v:
				nom = game_font.render("{}:".format(a), 1, (0, 0, 0))
				screen.blit(nom, (22+x+z, 414+y))
				stat = str(chars[a])
				nom = game_font.render(stat, 1, (0, 0, 0))
				if chars[a] <= 0:
					nom = game_font.render(stat, 1, (255, 0, 0))
				if a == "mor":
					m = 5
					if chars[a] >= 5: nom = game_font.render(stat, 1, (0, 100, 0))
				else:
					m = 0
					if chars[a] >= 10: nom = game_font.render(stat, 1, (0, 100, 0))
				screen.blit(nom, (60+m+x+z, 414+y))
				y += 29
			z += 70
		x += 152

def blitsupply(screen):
	supply =Misc.Loadsupply()
	cardx =572
	cardy = 170
	screen.blit(card(), (cardx, cardy))	
	screen.blit(fish(), (cardx+5, cardy+5))
	screen.blit(arrow(), (cardx+5, cardy+35))
	screen.blit(potion(), (cardx+5, cardy+65))
	screen.blit(gold(), (cardx+5, cardy+95))
	supp = ["food", "arrows", "potions", "gold"]
	y = 0
	for a in supp:
		nom = game_font.render("x{}".format(supply[a]), 1, (0, 0, 0))
		screen.blit(nom, (cardx+25, cardy +10+y))
		y +=30

def damage(char,screen,y):
	party = Misc.Loadparty()
	party[char]["hp"] -= 1
	if party[char]["hp"] <= 0:
		#death sound
		mes = "{0} took mortal damage and died!".format(party[char]["nome"])
		tex1 = game_font.render(mes, 1, (155, 0, 0))
		party.remove(party[char])
	else:
		#dmg sound
		mes = "{0} took damage!".format(party[char]["nome"])
		tex1 = game_font.render(mes, 1, (255, 0, 0))
	screen.blit(tex1, (100, y))
	pygame.display.update()
	time.sleep(0.8)
	Misc.Saveparty(party)