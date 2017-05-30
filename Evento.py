import pygame
from pygame.locals import *
from sys import exit
import time
import random
import Batalha
import Misc
import json


pygame.init()


pygame.font.init()
font_name = pygame.font.get_default_font()
game_font = pygame.font.Font("Treamd.ttf", 30)

def paper():
	return pygame.image.load('paper2.png').convert()

def arrow():
	return pygame.image.load('indic2.png').convert()

def endar():
	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

def statup(char,stat,screen,y):
	party = Misc.Loadparty()
	if party[char][stat] < 10:
		#raise sound
		party[char][stat]+=1
		mes = "{0}'s {1} went up!".format(party[char]["nome"],stat)
		tex1 = game_font.render(mes, 1, (0, 150, 0))
		screen.blit(tex1, (100, y))
		pygame.display.update()
		time.sleep(0.8)
	Misc.Saveparty(party)

def morale(char,many,screen,y):
	party = Misc.Loadparty()
	party[char]["mor"]+=many
	if many > 0:
		#raise sound
		mes = "{0}'s morale went up!".format(party[char]["nome"])
		tex1 = game_font.render(mes, 1, (0, 150, 0))
	else:
		#lower sound
		mes = "{0}'s morale went down!".format(party[char]["nome"])
		tex1 = game_font.render(mes, 1, (255, 0, 0))
	screen.blit(tex1, (100, y))
	pygame.display.update()
	time.sleep(0.8)
	Misc.Saveparty(party)

def getsupply(sup,many,screen,y):
	supply = Misc.Loadsupply()
	#raise sound
	supply[sup]+=many
	mes = "Got {0} {1}!".format(many,sup)
	tex1 = game_font.render(mes, 1, (0, 150, 0))
	screen.blit(tex1, (100, y))
	pygame.display.update()
	time.sleep(0.8)
	Misc.Savesupply(supply)

def meal(screen,y):
	party = Misc.Loadparty()
	supply = Misc.Loadsupply()
	#raise sound
	many = len(party)*2
	supply["food"]-=many
	mes = "Eaten {} food!".format(many)
	tex1 = game_font.render(mes, 1, (255, 0, 0))
	screen.blit(tex1, (100, y))
	pygame.display.update()
	time.sleep(0.8)
	Misc.Savesupply(supply)

def ration(screen,y):
	party = Misc.Loadparty()
	supply = Misc.Loadsupply()
	#raise sound
	mes = "Eaten {} food!".format(supply["food"])
	supply["food"] =0
	tex1 = game_font.render(mes, 1, (255, 0, 0))
	screen.blit(tex1, (100, y))
	pygame.display.update()
	time.sleep(0.8)
	Misc.Savesupply(supply)

def slowblit(str,screen,y):
	endar()
	clock = pygame.time.Clock()
	for a in range(len(str)+1):
		tex2 = game_font.render(str[:a], 1, (0, 0, 0))
		screen.blit(tex2, (100, y))
		pygame.display.update()
		time_passed = clock.tick(30)

def walloftext(Text,screen):
	screen.blit(paper(),(50,50))
	y=60
	for b in Text:
		slowblit(b,screen,y)
		y +=30
	return y

def proceed(screen):
	clock = pygame.time.Clock()
	while True:
		endar()
		tex = game_font.render("Proceed", 1, (0, 0, 0))
		screen.blit(tex, (285,300))
		screen.blit(arrow(), (275,295))
		pressed_keys = pygame.key.get_pressed()
		if pressed_keys[K_SPACE]:
			return
		pygame.display.update()
		time_passed = clock.tick(30)

def choose(choices,txt,screen):
	lag =0
	cursor = 1
	clock = pygame.time.Clock()
	while True:
		endar()
		y = 60
		screen.blit(paper(),(50,50))
		for linhas in txt:
			text = game_font.render(linhas, 1, (0, 0, 0))
			screen.blit(text, (100,y))
			y +=30
		tex1 = game_font.render(choices[0], 1, (0, 0, 0))
		screen.blit(tex1, (110,270))
		if len(choices) >= 2:
			tex2 = game_font.render(choices[1], 1, (0, 0, 0))
			screen.blit(tex2, (360,270))
		if len(choices) >= 3:
			tex3 = game_font.render(choices[2], 1, (0, 0, 0))
			screen.blit(tex3, (110,310))
		if len(choices) >= 4:
			tex4 = game_font.render(choices[3], 1, (0, 0, 0))
			screen.blit(tex4, (360,310))
		pressed_keys = pygame.key.get_pressed()
		if lag >=5:
			if pressed_keys[K_UP]:
				cursor -=2
				if cursor <= 0:
					cursor +=4
				lag = 0
			elif pressed_keys[K_DOWN]:
				cursor +=2
				if cursor > len(choices):
					cursor -=4
				lag = 0
			elif pressed_keys[K_LEFT]:
				cursor -=1
				if cursor <= 0:
					cursor +=4
				lag = 0
			elif pressed_keys[K_RIGHT]:
				cursor +=1
				if cursor > len(choices):
					cursor -=4
				lag = 0
			elif pressed_keys[K_SPACE]:
				return cursor
		if cursor > len(choices):
			cursor = len(choices)
		if cursor <=0:
			cursor = 1
		if cursor == 1:
			screen.blit(arrow(), (100,265))
		elif cursor == 2:
			screen.blit(arrow(), (350,265))
		elif cursor == 3:
			screen.blit(arrow(), (100,305))
		elif cursor == 4:
			screen.blit(arrow(), (350,305))
		lag+=1
		pygame.display.update()
		time_passed = clock.tick(30)
	

def charchoose(choices,txt,screen):
	party = Misc.Loadparty()
	for chars in party:
		choices.append(chars["nome"])
	return choose(choices,txt,screen)

def charjoin(char,screen,y):
	party = Misc.Loadparty()
	story = Misc.Loadstory()
	charlist = Misc.Charlist()
	if len(party) >= 4:
		slowblit("You have too many crew members.",screen,y)
	else:
		party.append(charlist[char])
		mes = "{0} joined the crew!".format(char)
		tex1 = game_font.render(mes, 1, (0, 150, 0))
		screen.blit(tex1, (100,y))
		pygame.display.update()
		time.sleep(0.8)
		Misc.Saveparty(party)
		story.append(char)
		Misc.Savestory(story)







def TrainSkl(screen):
	party = Misc.Loadparty()
	Text = ["The crew finds a practice target floating",
			"in the water. It's worn down and has", 
			"started to rot away, but hey, it will still", 
			"likely make for some good practice",
			"",
			"Who should try to train their aim?"]
	y=60
	y = walloftext(Text,screen)
	choices = []
	chari = charchoose(choices,Text,screen)
	char = chari-1
	out = random.randint(0,1)
	if out == 0:
		text = ["{} gets some good practice with the".format(party[char]["nome"]), "target before a shot snaps it in two."]
	if out == 1:
		text = ["{} shoots the target a few times".format(party[char]["nome"]),"before it gets irreparably damaged."]
	y =60
	screen.blit(paper(),(50,50))
	for c in text:
		slowblit(c,screen,y)
		y +=30
	statup(char,"skl",screen,y)
	proceed(screen)

def Castaway(screen):
	party = Misc.Loadparty()
	story =Misc.Loadstory()
	possible = ["Leozin","Minos"]
	char = party[0]["nome"]
	c =0
	while char in story:
		char = possible[random.randint(0,len(possible)-1)]
		c +=1
		if c >= (len(possible)+2):
			Text = ["The ship passes by a small deserted islet.",
				"The island is completely empty aside.", 
				"from a couple of coconut trees.", 
				"The crew help themselves to the",
				"coconuts."]
			y = walloftext(Text,screen)
			getsupply("food",4,screen,y)
			proceed(screen)
			return
	Text = ["The ship passes by a small deserted islet.",
			"It seems there's someone stuck there.", 
			"The person introduces themselves as", 
			"{}, it seems he was cast away for".format(char),
			"quite some time.",
			"Allow {} to join your crew?".format(char)]
	y = walloftext(Text,screen)
	choices = ["Yes","No"]
	YN = choose(choices,Text,screen)
	screen.blit(paper(),(50,50))
	y = 60
	if YN == 1:
		charjoin(char,screen,y)
		proceed(screen)

def Magicbo(screen):
	party = Misc.Loadparty()
	Text = ["It's Bo, the magical sword instructor!",
			"He just appeared out of thin air onto", 
			"the boat. He offers to train the", 
			"crew for free! What luck!",
			"",
			"What should you train?"]
	y = walloftext(Text,screen)
	choices = ["Strength","Skill","Intelligence"]
	a = choose(choices,Text,screen)
	screen.blit(paper(),(50,50))
	if a == 1:
		stat = "str"
		Text = ["Bo runs the party through a",
				"fabulous weight lifting routine.", 
				"They'll be buff as a bull in no time!"]
	elif a == 2:
		stat = "skl"
		Text = ["With Bo's help, the party trains",
				"until they can each balance two", 
				"swords on their noses."]
	elif a == 3:
		stat = "int"
		Text = ["Bo hands the party a challenging",
				"yet interesting crossword puzzle.", 
				"Working together, the crew solves it",
				"with 'some' handholding."]
	y=60
	for b in Text:
		slowblit(b,screen,y)
		y +=30
	for c in range(len(party)):
		statup(c,stat,screen,y)
		y+=30
	proceed(screen)

def Newspaper(screen):
	party = Misc.Loadparty()
	Text = ["A seagull delivers the newest edition",
			"of the 'Tidal Times' newspaper to", 
			"the ship. It looks very interesting.",
			"",
			"Who should take it?"]
	y = walloftext(Text,screen)
	choices = []
	char = charchoose(choices,Text,screen)-1
	screen.blit(paper(),(50,50))
	Text = ["Which part of the newspaper",
			"should {} read first?".format(party[char]["nome"])]
	y = walloftext(Text,screen)
	choic = ["The funnies","The latest news","The crosswords","Just toss it away"]
	choices = choose(choic,Text,screen)
	outc = random.randrange(1,10)
	if choices == 1:
		if outc < 5:
			Text = ["{} read the funnies, but they".format(party[char]["nome"]),
					"weren't funny at all.",
					"{} tosses the newspaper away".format(party[char]["nome"]),
					"in frustration"]
			y = walloftext(Text,screen)
			morale(char,-1,screen,y)
		else:
			Text = ["{} laughed so hard that".format(party[char]["nome"]),
					"the newspaper accidently fell ",
					"overboard."]
			y = walloftext(Text,screen)
			morale(char,2,screen,y)
	elif choices == 2:
		if outc <6:
			Text = ["After reading the latest news",
					"{} lost some of their".format(party[char]["nome"]),
					"faith in humanity. They throw",
					"the newspaper away in disgust."]
			y = walloftext(Text,screen)
			morale(char,-2,screen,y)
		elif outc <8:
			Text = ["It seems there's a lot of stuff",
					"going on in the world, but none",
					"of it matter to {}.".format(party[char]["nome"]),
					"{} misplaces the newpaper after".format(party[char]["nome"]),
					"growing bored with it."]
			y = walloftext(Text,screen)
		else:
			Text = ["There seems to be approximately",
					"a thousand wars going on in the",
					"world. On the plus side, it seems",
					"nobody has found the treasure yet",
					"so that's good news."]
			y = walloftext(Text,screen)
			morale(char,3,screen,y)
	elif choices == 3:
		outc -= 3
		if outc > party[char]["int"]:
			Text = ["{} tries to solve the crosswords,".format(party[char]["nome"]),
					"but isn't able to over a very",
					"long time. {} tosses the".format(party[char]["nome"]),
					"newspaper away in frustration."]
			y = walloftext(Text,screen)
			morale(char,-1,screen,y)
		else:
			Text = ["After a long time trying to solve",
					"the crosswords, {} finally does it!".format(party[char]["nome"]),
					"They throw the newspaper up in celebration.",
					"Unfortunately, the wind carries the",
					"newspaper away into the sea."]
			y = walloftext(Text,screen)
			statup(char,"int",screen,y)
	else:
		Text = ["{} tosses the newspaper away.".format(party[char]["nome"])]
		y = walloftext(Text,screen)
	proceed(screen)


def Suicide(char,screen):
	party = Misc.Loadparty()
	Text = ["Crushed by their desperate situation",
					"at sea, {} decides to end their ".format(party[char]["nome"]),
					"own life."]
	y = walloftext(Text,screen)
	party =Misc.Loadparty()
	if len(party) >1:
		choices = ["Don't do it!","Good riddance!"]
		ra = choose(choices,Text,screen)
		outco = random.randrange(10)
		if ra == 1:
			if outco>=6:
				Text = ["Moved by their crewmate's care",
							"for them, {} decides to go on".format(party[char]["nome"]),
							"living for a while longer."]
				y = walloftext(Text,screen)
				morale(char,2,screen,y)
			elif outco>=3:
				Text = ["{} decides to go through with",
							"it despite their crewmates' pleas.",
							"But the rope they use to hang"
							"themselves is rotten and breaks",
							"halfway through the attempt."]
				y = walloftext(Text,screen)
				Battle.damage(char,screen,y)
			else:
				Text = ["{} isn't swayed.".format(party[char]["nome"]),
							"{} simply jumps of the boat".format(party[char]["nome"]),
							"and fades into the ocean."]
				y = walloftext(Text,screen)
				party.remove(party[char])
				Misc.Saveparty(party)
				for ar in party:
					morale(char,-1,screen,y)
					y +=30
		if ra == 2:
			if outco >= 6:
				Text = ["{} goes and jumps off the boat".format(party[char]["nome"]),
							"much to the others delight"]
				y = walloftext(Text,screen)
				party.remove(party[char])
				for ar in party:
					morale(char,1,screen,y)
					y +=30
			elif outco >= 3:
				Text = ["{} unexpectedly jumps off the boat,".format(party[char]["nome"]),
							"and everyone else feels very guilty",
							"about it."]
				y = walloftext(Text,screen)
				party.remove(party[char])
				for ar in party:
					morale(char,-2,screen,y)
					y +=30
			else:
				Text = ["{}, sees what everyone thinks of them".format(party[char]["nome"]),
							"and vows to not end their life before",
							"making them care."]
				y = walloftext(Text,screen)

		Text = ["{} attempts suicide by hanging".format(party[char]["nome"]),
				"but the rope they used was rotted",
				"and snapped.",
				"{} crashes to the floor".format(party[char]["nome"])]
		y = walloftext(Text,screen)
		Battle.damage(char,screen,y)
	proceed(screen)


def	Eatfood(screen):
	Text = ["The crew eats a hearty meal after",
			"a long day of sailing."]
	y = walloftext(Text,screen)
	meal(screen,y)
	proceed(screen)

def	Feast(screen):
	party = Misc.Loadparty()
	if len(party) >1:
		Text = ["The crew has a feast at daybreak",
			"to celebrate their survival."]
		y = walloftext(Text,screen)
		
		choices = ["Sing a song","Tell stories"]
		act = choose(choices,Text,screen)
		out = random.randint(0,10)
		if act == 1:
			if out >7:
				Text = ["The crew all come together to",
				"sing a sailor's song and have a.",
				"gay old time."]
				y = walloftext(Text,screen)
				for char in range(len(party)):
					morale(char,2,screen,y)
					y+=30
			elif out >4:
				Text = ["They all sing a sailor's song,",
					"but the quality of the song depends",
					"on the listener's state of mind."]
				y = walloftext(Text,screen)
				for char in range(len(party)):
					if party[char]["mor"]>=3:
						morale(char,1,screen,y)
					else:
						morale(char,-1,screen,y)
					y+=30
			else:
				Text = ["In their intoxicated state,",
					"their song becomes less a song",
					"and more a ininteligible moan."]
				y = walloftext(Text,screen)
				morale(char,-1,screen,y)
		if act == 2:
			char1 = random.randrange(len(party))
			if out <5:
				char2 = char1
				while char2 == char1:
					char2 = random.randrange(len(party))
				if party[char1]["int"] < party[char2]["int"]:
					learner = char1
					teacher = char2
				else:
					learner = char1
					teacher = char2
				Text = ["{0} teaches {1} about the stars".format(party[teacher]["nome"],party[learner]["nome"]),
					"and the wisdom of the sea."]
				y = walloftext(Text,screen)
				statup(learner,"int",screen,y)
			elif out < 9:
				Text = ["{0} recounts the story of the".format(party[char1]["nome"]),
					"gigantic fish he once almost caught.",
					"no one believes him, but they all",
					"have a good time anyway."]
				y = walloftext(Text,screen)
				for char in range(len(party)):
					morale(char,1,screen,y)
					y+=30
			else:
				Text=["{} recounts a depressing story".format(party[char1]["nome"]),
						"about their past."]
				y = walloftext(Text,screen)
				for char in range(len(party)):
					morale(char,-1,screen,y)
					y+=30
	else:
		Text = ["{} eats a lavish meal alone.".format(party[0]["nome"])]
		y =walloftext(Text,screen)
	meal(screen,y)
	proceed(screen)

def Rationfood(screen):
	party = Misc.Loadparty()
	Text = ["The crew doesn't have enough food",
			"to feed everyone, so they have to",
			"ration it."]
	y = walloftext(Text,screen)
	for char in range(len(party)):
		morale(char,-2,screen,y)
		y+=30
	ration(screen,y)
	proceed(screen)

def Foodfight(screen):
	party = Misc.Loadparty()
	if len(party) > 1:
		Text = ["The remaining supplies aren't enough",
			"to feed everyone, so a fight to determine",
			"who gets the last scraps ensues."]
		y = walloftext(Text,screen)
		char = random.randrange(len(party))
		Batalha.damage(char,screen,y)
		y +=30
		char = random.randrange(len(party))
		Batalha.damage(char,screen,y)
		y +=30
	else:
		Text = ["{} doesn't have enough food for".format(party[0]["nome"]),
			"the day, but at least he doesn't.",
			"have to share it with anybody."]
		y = walloftext(Text,screen)
	for char in range(len(party)):
		morale(char,-1,screen,y)
		y+=30
	ration(screen,y)
	proceed(screen)

def Starving(screen):
	Text = ["The crew suffers hunger pains from the",
			"lack of food."]
	party = Misc.Loadparty()
	y = walloftext(Text,screen)
	for char in range(len(party)):
		Batalha.damage(char,screen,y)
		y+=30
	for char in range(len(party)):
		morale(char,-1,screen,y)
		y+=30
	proceed(screen)

def Cannibal(screen):
	party = Misc.Loadparty()
	if len(party) > 1:
		Text = ["Mad from the hunger, the party decides",
			"to cannibalise someone. Who should",
			"be eaten first?"]
		choices = []
		char = charchoose(choices,Text,screen)
		char -=1
		Text = ["{} is eaten by his fellow crewmembers.".format(party[char]["nome"]),
			"Everyone can eat, and there is even a",
			"little left over!"]
		#death sound
		y = walloftext(Text,screen)
		party.remove(party[char])
		Misc.Saveparty(party)
		for char in range(len(party)):
			morale(char,-1,screen,y)
			y+=30
		getsupply("food",2,screen,y)

	else:
		Text = ["The hunger leads {} to start eating".format(party[0]["nome"]),
			"their own body."]
		y = walloftext(Text,screen)
		Batalha.damage(0,screen,y)
		Batalha.damage(0,screen,y)
	proceed(screen)