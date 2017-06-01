import pygame
from pygame.locals import *
#import Evento
from sys import exit
import time
import random
#import Batalha
import json

def Save(party,supply,ship,position,story):
	Sav = {"party":party,"supply":supply,"ship":ship,"pos":position,"story":story}
	with open("Save.json", "w") as Arq:
		json.dump(Sav,Arq)

def Getenemy(enemy):
	with open("enemy.json", "r") as Enn:
		ini = json.load(Enn)
	return ini[enemy]

def Charlist():
	with open("chars.json", "r") as Arq:
		sav = json.load(Arq)
	return sav

def Loadparty():
	with open("save.json", "r") as Arq:
		sav = json.load(Arq)
	return sav["party"]

def Loadsupply():
	with open("save.json", "r") as Arq:
		sav = json.load(Arq)
	return sav["supply"]

def Loadship():
	with open("save.json", "r") as Arq:
		sav = json.load(Arq)
	return sav["ship"]

def Loadpos():
	with open("save.json", "r") as Arq:
		sav = json.load(Arq)
	return sav["pos"]

def Loadstory():
	with open("save.json", "r") as Arq:
		sav = json.load(Arq)
	return sav["story"]

def Saveparty(party):
	Save(party,Loadsupply(),Loadship(),Loadpos(),Loadstory())

def Savesupply(supply):
	Save(Loadparty(),supply,Loadship(),Loadpos(),Loadstory())

def Saveship(ship):
	Save(Loadparty(),Loadsupply(),ship,Loadpos(),Loadstory())

def Savepos(pos):
	Save(Loadparty(),Loadsupply(),Loadship(),pos,Loadstory())

def Savestory(story):
	Save(Loadparty(),Loadsupply(),Loadship(),Loadpos(),story)