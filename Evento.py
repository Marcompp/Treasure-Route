import pygame
from pygame.locals import *
from sys import exit
import time
import random
import Batalha
import Misc
import json
import Classes as CT


pygame.init()


pygame.font.init()
font_name = pygame.font.get_default_font()
game_font = pygame.font.Font("Treamd.ttf", 30)

def paper():
	return pygame.image.load('paper2.png').convert()

def arrow():
	return pygame.image.load('indic2.png')

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
		CT.Som("level_up.ogg")
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
	if party[char]["mor"] >5:
		party[char]["mor"] = 5
	if party[char]["mor"] <0:
		party[char]["mor"] = 0
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

def losesupply(sup,many,screen,y):
	supply = Misc.Loadsupply()
	#raise sound
	supply[sup]-=many
	mes = "Lost {0} {1}!".format(many,sup)
	tex1 = game_font.render(mes, 1, (255, 0, 0))
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


def	Battletest(screen):
	Text = ["The boat is set upon by a pirate",
			"ship. A single pirate manages to",
			"get on board and attacks the crew!"]
	y = walloftext(Text,screen)
	proceed(screen)
	Batalha.battle(["Pirate"],screen)
	proceed(screen)



def Newgame(screen):
	Text = ["Mayara after hearing many tales",
					"about the legendary treasure left",
					"behind by the pirate king",
					"Howell D'Or, said contain enough",
					"gold to buy an entire kingdon,",
					"decides to go after it. She talks",
					"her childhood friend Juju into it,",
					"and sets sail into the sea!"]
	y = walloftext(Text,screen)
	proceed(screen)
	Text = ["The ocean is fraught with danger at",
					"every turn. Only by making the",
					"right decisions and carefully managing",
					"managing may you have a shat at",
					"surviving your trip and making it",
					" to Howell D'Or's treasure!"]
	proceed(screen)


def Goal(screen):
	Text = ["After enduring many, many, many hardships,",
	"the crew finally arrives at Blue Pearl",
	"Island, where Howell D'Or's treasure is",
	"said to rest. It they find it, they should",
	"have enough gold to buy a kingdom."]
	y = walloftext(Text,screen)
	proceed(screen)

	Text = ["The crew uses everything they learned up",
	"until this point to find the treasure",
	"chest's hiding place."]
	y = walloftext(Text,screen)
	proceed(screen)

	Text = ["Expectation builds as they open it."]
	y = walloftext(Text,screen)
	proceed(screen)

	Text = ["Inside is... a straw hat alongside",
	"a note. It said some rubbish about the",
	"adventure to get here and your companions",
	"on this journey being the real treasure",
	"and, at the very end of the note, it was",
	"written: 'PS. I don't actually have gold'"]
	y = walloftext(Text,screen)
	proceed(screen)
	Text = ["The crew is disappointed to say the",
	"least, but when they think of what to",
	"do next, they don't even consider going",
	"back the way they came, so instead, they",
	"decide to settle down on the island."]
	y = walloftext(Text,screen)
	proceed(screen)
	Text = ["Years later, their little settlement",
	"grew to become a great kingdom.",
	"Though they did not get enough",
	"gold to buy a kingdom, they did get",
	"a kingdom in the end.",
	"Too bad none of them lived to see it."]
	y = walloftext(Text,screen)
	proceed(screen)
	Text = "THE END"
	y = walloftext(Text,screen)
	proceed(screen)

def TrainInt(screen):
	party = Misc.Loadparty()
	Text = ["The crew finds a small box floating",
			"in the ocean. Inside is a book,", 
			"badly damaged by the water. It", 
			"looks to be a very rare volume.",
			"",
			"Who should try and read it?"]
	y=60
	y = walloftext(Text,screen)
	choices = []
	chari = charchoose(choices,Text,screen)
	char = chari-1
	out = random.randint(0,2)
	if out == 0:
		text = ["The book turns out to be a 'How To'",
						"guide on how to follow the stars.",
						"{} absorbs as much knowledge as they".format(party[char]["nome"]),
						"can before the book falls apart."]
	if out == 1:
		text = ["The book is an extremely rare copy",
						"of 'Basic Calculus for Dummies' by",
						"Carlon the Matemagician. {}".format(party[char]["nome"]),
						"reads it front to back, but is only",
						"able to understand a little before",
						"the book is destroyed."]
	if out == 2:
		text = ["The book turns out to be a math book",
						"for children. {} finds the".format(party[char]["nome"]),
						"book very helpful while it lasts."]
	y =60
	y = walloftext(text,screen)
	statup(char,"int",screen,y)
	proceed(screen)

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

def TrainStr(screen):
	party = Misc.Loadparty()
	Text = ["The crew produces some dumbells",
			"out of fish bones and sticks so they", 
			"can get fit.", 
			"",
			"Who should try lifting first?"]
	y=60
	y = walloftext(Text,screen)
	choices = []
	chari = charchoose(choices,Text,screen)
	char = chari-1
	out = random.randint(0,1)
	if out == 0:
		text = ["{} gets some lifting in before".format(party[char]["nome"]), "before the dumbells just fall apart.",
						"Who would've though making fitness","equipment out of fish bones and sticks","was a bad idea?"]
	if out == 1:
		text = ["{} doesn't seem to grasp the concept".format(party[char]["nome"]),"of lifting weight, and instead uses all",
				"their power to throw the dumbells as","as far as they can and into the sea."]
	y =60
	screen.blit(paper(),(50,50))
	for c in text:
		slowblit(c,screen,y)
		y +=30
	statup(char,"str",screen,y)
	proceed(screen)

def Rowboat(screen):
	party = Misc.Loadparty()
	story =Misc.Loadstory()
	possible = ["Marcones","Jane"]
	char = party[0]["nome"]
	c =0
	while char in story:
		char = possible[random.randint(0,len(possible)-1)]
		c +=1
		if c >= (len(possible)+2):
			Text = ["A small rowboat appears in the horizon.",
							"It looks to be empty at first, but as it", 
							"gets closer the crew can see there's a", 
							"box with some gold in it. Maybe someone",
							"saved their belongings before",
							"saving themselves?."]
			y = walloftext(Text,screen)
			getsupply("gold",2,screen,y)
			proceed(screen)
			return
	Text = ["A small rowboat appears in the horizon.",
			"There seems to be someone passed out", 
			"inside! It's {}, who claims to have".format(char), 
			"just survived a shipwreck and now wants",
			"to come with you.",
			"Allow {} to join your crew?".format(char)]
	y = walloftext(Text,screen)
	choices = ["Yes","No"]
	YN = choose(choices,Text,screen)
	screen.blit(paper(),(50,50))
	y = 60
	if YN == 1:
		charjoin(char,screen,y)
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
	choices = ["Strength","Intelligence","Skill"]
	a = choose(choices,Text,screen)
	screen.blit(paper(),(50,50))
	if a == 1:
		stat = "str"
		Text = ["Bo runs the party through a",
				"fabulous weight lifting routine.", 
				"They'll be buff as a bull in no time!"]
	elif a == 3:
		stat = "skl"
		Text = ["With Bo's help, the party trains",
				"until they can each balance two", 
				"swords on their noses."]
	elif a == 2:
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

def Fishday(screen):
	party = Misc.Loadparty()
	Text = ["The crew decides to make a stop",
					"to do some fishing.",
					""
					"They could either try and fish using a",
					"makeshift fishing rod or try to set up",
					"some fish nets."]
	y = walloftext(Text,screen)
	choices = ["Use fishing rod","Use fish net"]
	met = choose(choices,Text,screen)
	fish = random.randrange(9)
	choices = []
	if met ==1:
		Text = ["Who should try their hand at fishing?",
						"A strong and stead hand is essential."]
		y = walloftext(Text,screen)
		char = charchoose(choices,Text,screen)-1
		if fish >= party[char]["str"]:
			Text = ["{} casts out the fishing rod and".format(party[char]["nome"]),
							"waits until finally getting a bite.",
							"Unfortunately the fish is to strong",
							"for {} and they let go of the".format(party[char]["nome"]),
							"fishing rod, losing it."]
			y = walloftext(Text,screen)
			proceed(screen)
		elif fish >= 7:
			Text = ["{} casts out the fishing rod and".format(party[char]["nome"]),
							"waits until finally getting a bite.",
							"The fish who took the bait is",
							"gigantic and way too strong, but",
							"{} is able to pull it aboard,".format(party[char]["nome"]),
							"breaking the fishing rod in the process."]
			y = walloftext(Text,screen)
			getsupply("food",9,screen,y)
			proceed(screen)
		elif fish >= 4:
			Text = ["{} casts out the fishing rod and".format(party[char]["nome"]),
							"waits until finally getting a bite.",
							"They are able to catch a medion sized",
							"fish, before the rod snaps."]
			y = walloftext(Text,screen)
			getsupply("food",5,screen,y)
			proceed(screen)
		elif fish >= 2:
			Text = ["{} casts out the fishing rod and".format(party[char]["nome"]),
							"waits until finally getting a bite.",
							"After a long struggle, they pull up",
							"a tiny, pathetic fish at the cost",
							"of the fishing rod."]
			y = walloftext(Text,screen)
			getsupply("food",2,screen,y)
			proceed(screen)
		else:
			Text = ["{} casts out the fishing rod and".format(party[char]["nome"]),
							"waits for a long time, but no fish",
							"ever show up.",
							"Maybe using an old boot as bait was",
							"a bad idea?"]
			y = walloftext(Text,screen)
			proceed(screen)
	elif met ==2:
		Text = ["Who should try set up the fish net?",
						"Precision and the ability to make", "cool knots are essential."]
		y = walloftext(Text,screen)
		char = charchoose(choices,Text,screen)-1
		if fish >= party[char]["skl"]:
			Text = ["{} sets up the fish net with care,".format(party[char]["nome"]),
							"But its ripped when they come back",
							"to check on it..."]
			y = walloftext(Text,screen)
			proceed(screen)
		elif fish >= 2:
			Text = ["{} casts out the fishing net and".format(party[char]["nome"]),
							"manages to catch a whole bunch of",
							"fish with it."]
			y = walloftext(Text,screen)
			getsupply("food",6,screen,y)
			proceed(screen)
		else:
			Text = ["{} sets up the fishing net, but".format(party[char]["nome"]),
							"it never manages to catch a single",
							"fish even after being cast out",
							"for a long time."]
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
				Text = ["{} decides to go through with".format(party[char]["nome"]),
							"it despite their crewmates' pleas.",
							"But the rope they use to hang",
							"themselves is rotten and breaks",
							"halfway through the attempt."]
				y = walloftext(Text,screen)
				Batalha.damage(char,screen,y)
			else:
				Text = ["{} isn't swayed.".format(party[char]["nome"]),
							"{} simply jumps of the boat".format(party[char]["nome"]),
							"and fades into the ocean."]
				y = walloftext(Text,screen)
				party.remove(party[char])
				Misc.Saveparty(party)
				for ar in range(len(party)):
					morale(ar,-1,screen,y)
					y +=30
		if ra == 2:
			if outco >= 6:
				Text = ["{} goes and jumps off the boat".format(party[char]["nome"]),
							"much to the others delight"]
				y = walloftext(Text,screen)
				party.remove(party[char])
				Misc.Saveparty(party)
				for ar in range(len(party)):
					morale(ar,1,screen,y)
					y +=30
			elif outco >= 3:
				Text = ["{} unexpectedly jumps off the boat,".format(party[char]["nome"]),
							"and everyone else feels very guilty",
							"about it."]
				y = walloftext(Text,screen)
				party.remove(party[char])
				Misc.Saveparty(party)
				for ar in range(len(party)):
					morale(ar,-2,screen,y)
					y +=30
			else:
				Text = ["{}, sees what everyone thinks of them".format(party[char]["nome"]),
							"and vows to not end their life before",
							"making them care."]
				y = walloftext(Text,screen)
	else:
		proceed(screen)
		Text = ["{} attempts suicide by hanging".format(party[char]["nome"]),
				"but the rope they used was rotted",
				"and snapped.",
				"{} crashes to the floor".format(party[char]["nome"])]
		y = walloftext(Text,screen)
		Batalha.damage(char,screen,y)
	proceed(screen)

def Pullweight(char,screen):
	party = Misc.Loadparty()
	if len(party) >=3:
		Text = ["Frustrated with the crew's situation,",
						"{} says that SOMEONE hasn't been".format(party[char]["nome"]),
						"pulling their weight and are making",
						"everyone else miserable, so they",
						"demand that someone be kicked from",
						"the boat.",
						"Who should be kicked out?"]
		y = walloftext(Text,screen)
		choices = []
		exp = charchoose(choices,Text,screen) - 1
		if exp == char:
			Text = ["Despite {}'s repeated claims that".format(party[exp]["nome"]),
							"they were just joking, the others",
							"kick'em out anyway.",
							"",
							"Everyone is glad to see them gone."]
		else:
			Text = ["The crew decides to kick {} out".format(party[exp]["nome"]),
							"for no reason. {} is heartbroken,".format(party[exp]["nome"]),
							"but nobody liked'em anyway."]
		y = walloftext(Text,screen)
		party.remove(party[exp])
		Misc.Saveparty(party)
		for ar in range(len(party)):
			morale(ar,2,screen,y)
			y +=30
	else:
			Text = ["{} is depressed and feels that".format(party[char]["nome"]),
							"they aren't working hard enough",
							"to achieve their goal. In order",
							"to turn over a new leaf, {}".format(party[char]["nome"]),
							"tosses away most of their stuff."]
			y = walloftext(Text,screen)
			supply = Misc.Loadsupply()
			sups = ["arrows","potions"]
			for a in sups:
				many = int(supply[a]/2)
				losesupply(a,many,screen,y)
				y+=30
			morale(char,2,screen,y)
	proceed(screen)


def	Eatfood(screen):
	Text = ["The crew eats a hearty meal after",
			"a long day of sailing."]
	y = walloftext(Text,screen)
	meal(screen,y)
	proceed(screen)

def	Eatsup(screen):
	Text = ["The crew eats some of their food",
			"supplies at the end of the day."]
	y = walloftext(Text,screen)
	meal(screen,y)
	proceed(screen)

def	Alcoffering(screen):
	party = Misc.Loadparty()
	Text=["The crew spots an offering barrel drifting",
				"in the waves. There's likely alcohool",
				"inside the barrel, but stealing it",
				"may anger the spirits of the dead."]
	y = walloftext(Text,screen)
	choices = ["Drink the mead","Leave it alone"]
	act = choose(choices,Text,screen)
	if act == 1:
		outc = random.randrange(10)
		if outc >=5:
			Text=["The crew pulls the offering barrel",
					"aboard and drink the mead instead",
					"of eating. They all have a great",
					"time."]
			walloftext(Text,screen)
			for char in range(len(party)):
					morale(char,1,screen,y)
					y+=30
		else:
			Text=["The crew pulls the offering barrel",
					"aboard and drink the mead instead",
					"of eating. But when they're done",
					"they hear a ghastly voice and",
					"are really creeped out."] 
			walloftext(Text,screen)
			for char in range(len(party)):
					morale(char,-2,screen,y)
					y+=30
	else:
		Text=["The crew try their best to ignore",
				"the offering barrel as they eat",
				"their dinner. Eventually, the barrel",
				"is carried away by the ocean."]
		walloftext(Text,screen)
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
				y += 30
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
		y = walloftext(Text,screen)
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