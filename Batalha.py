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

def slot():
	return pygame.transform.scale(card(),(130,100))

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

def healhp(char,heal,screen,y):
	party = Misc.Loadparty()
	party[char]["hp"] += heal
	#dmg sound
	mes = "{0} recovered {1} hp!".format(party[char]["nome"],heal)
	tex1 = game_font.render(mes, 1, (0, 150, 0))
	screen.blit(tex1, (100, y))
	pygame.display.update()
	time.sleep(0.8)
	Misc.Saveparty(party)

def damagenemy(foes,enemy,dmg,screen,y,crit):
	foes[enemy]["hp"] -= dmg
	if foes[enemy]["hp"] <= 0:
		#death sound
		mes = "{0} was defeated!!!".format(foes[enemy]["nome"])
		if crit == 1: tex1 = game_font.render(mes, 1, (0, 0, 0))
		if crit == 3: tex1 = game_font.render(mes, 1, (255, 0, 0))
		party.remove(Foes[enemy])
	else:
		#dmg sound
		mes = "{0} took {1} damage!".format(foes[enemy]["nome"],dmg)
		if crit == 1: tex1 = game_font.render(mes, 1, (0, 0, 0))
		if crit == 3: tex1 = game_font.render(mes, 1, (255, 0, 0))
	screen.blit(tex1, (100, y))
	pygame.display.update()
	time.sleep(0.8)
	return Foes

def strike(Foes,enemy,char,screen):
	party = Misc.Loadparty()
	hit = random.randrange(5)
	crit = 1
	if party[char]["skl"] >= hit:
		if party[char]["mor"] >= random.randrange(10): crit = 3
		dmg = (party[char]["str"]-Foes[enemy]["def"])*crit
		Foes = damagenemy(Foes,enemy,dmg,screen,60,crit)
	else:
		mes = "The attack missed!"
		tex1 = game_font.render(mes, 1, (0, 0, 0))
		screen.blit(tex1, (100, 60))
		time.sleep(0.8)
	time.sleep(0.8)
	return Foes

def shoot(Foes,enemy,char,screen):
	party = Misc.Loadparty()
	supply = Misc.Loadsupply()
	if supply["arrow"] > 0:
		supply["arrow"]-=1
		hit = random.randrange(5)
		crit = 1
		if party[char]["skl"] >= hit:
			if party[char]["mor"] >= random.randrange(10): crit = 3
			dmg = (party[char]["skl"]+party[char]["skl"]-Foes[enemy]["def"])*crit
			Foes = damagenemy(Foes,enemy,dmg,screen,60,crit)
		else:
			mes = "The attack missed!"
			tex1 = game_font.render(mes, 1, (0, 0, 0))
			screen.blit(tex1, (100, 60))
			time.sleep(0.8)
		time.sleep(0.8)
	else:
		mes = "You don't have any arrows!"
		tex1 = game_font.render(mes, 1, (0, 0, 0))
		screen.blit(tex1, (100, 60))
		time.sleep(0.8)
	Misc.Savesupply(supply)
	time.sleep(0.8)
	return Foes

def shoot(Foes,healee,char,screen):
	party = Misc.Loadparty()
	supply = Misc.Loadsupply()
	if party[char]["int"] == 10: need =0
	elif party[char]["int"] >= 6: need =1
	elif party[char]["int"] >= 4: need =2
	elif party[char]["int"] >= 2: need =3
	else: need =4
	if supply["potion"] >= need:
		supply["arrow"]-= need
		healed = int(party[char]["int"]/3)
		healhp(healee,healed,screen,60)
		time.sleep(0.8)
	else:
		mes = "You don't have enough potions!"
		tex1 = game_font.render(mes, 1, (0, 0, 0))
		screen.blit(tex1, (100, 60))
		time.sleep(0.8)
	Misc.Savesupply(supply)
	time.sleep(0.8)

def blitenemies(foes,screen):
	xpos = [255,100,450]
	ypos = [120,100,100]
	for enemy in range(len(foes)):
		imag= pygame.image.load(foes[enemy]["img"]).convert_alpha()
		screen.blit(imag,(xpos[enemy],ypos[enemy]))


def command(char,screen):
	x = 152 * char
	lag = 3
	cursor = 1
	clock = pygame.time.Clock()
	while True:
		Evento.endar()
		screen.blit(slot(), (22+x, 251))
		options = ["Strike","Shoot","Heal"]
		y = 0
		for test in options:
			tex1 = game_font.render(test, 1, (0, 0, 0))
			screen.blit(tex1,(47+x, 258+y))
			y += 30
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
			cursor = 1
		if cursor <=0:
			cursor = len(options)
		if cursor == 1:
			screen.blit(Evento.arrow(), (32+x,253))
		elif cursor == 2:
			screen.blit(Evento.arrow(), (32+x,253+30))
		elif cursor == 3:
			screen.blit(Evento.arrow(), (32+x,253+60))
		lag+=1
		pygame.display.update()
		time_passed = clock.tick(30)

def choosenemy(foes,screen):
	lag = 3
	cursor = 1
	clock = pygame.time.Clock()
	while True:
		Evento.endar()
		screen.blit(Evento.paper(),(50,50))
		blitcards(screen)
		blitsupply(screen)
		blitenemies(foes,screen)
		pressed_keys = pygame.key.get_pressed()
		if lag >=5:
			if pressed_keys[K_UP]:
				cursor -=1
				lag = 0
			elif pressed_keys[K_DOWN]:
				cursor +=1
				lag = 0
			elif pressed_keys[K_LEFT]:
				cursor +=1
				lag = 0
			elif pressed_keys[K_RIGHT]:
				cursor -=1
				lag = 0
			elif pressed_keys[K_SPACE]:
				return cursor
		if cursor > len(foes):
			cursor = 1
		if cursor <=0:
			cursor = len(foes)
		if cursor == 1:
			screen.blit(Evento.arrow(), (260,120))
		elif cursor == 2:
			screen.blit(Evento.arrow(), (105,100))
		elif cursor == 3:
			screen.blit(Evento.arrow(), (455,100))
		lag+=1
		pygame.display.update()
		time_passed = clock.tick(30)

def chooseally(foes,screen):
	party = Misc.Loadparty()
	lag = 3
	cursor = 1
	clock = pygame.time.Clock()
	while True:
		Evento.endar()
		screen.blit(Evento.paper(),(50,50))
		blitcards(screen)
		blitsupply(screen)
		blitenemies(foes,screen)
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
		if cursor > len(party):
			cursor = 1
		if cursor <=0:
			cursor = len(party)
		if cursor == 1:
			screen.blit(Evento.arrow(), (33,355))
		elif cursor == 2:
			screen.blit(Evento.arrow(), (33+152,355))
		elif cursor == 3:
			screen.blit(Evento.arrow(), (33+152+152,355))
		elif cursor == 4:
			screen.blit(Evento.arrow(), (33+152+152+152,355))
		lag+=1
		pygame.display.update()
		time_passed = clock.tick(30)


def battle(enemies,screen):
	Foes =[]
	Turn = ["play",0]
	for enemy in enemies:
		Foes.append(Misc.Getenemy(enemy))
	while True:
		Evento.endar()
		screen.blit(Evento.paper(),(50,50))
		blitcards(screen)
		blitsupply(screen)
		blitenemies(Foes,screen)
		if Turn[0] =="play":
			act = command(Turn[1],screen)
			if act == 1 or act == 2:
				target = choosenemy(Foes,screen)
			elif act == 3:
				target = chooseally(Foes,screen)
			if act ==1:
				Foes =  strike(Foes,target,Turn[1],screen)
		pygame.display.update()