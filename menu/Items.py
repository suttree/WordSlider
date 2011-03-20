#! /usr/bin/env python

import os
import sys
import time
import pygame
import webbrowser
from pygame.locals import *

FONT = os.path.join('fonts', 'nrkis.ttf')

class Bonus(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.off_screen = 0
		self.last_update = 0
		self.colours = [ [255,255,0], [255,128,0], [255,255,0], [255,128,0], [255,255,0], [255,128,0] ]
		self.font = pygame.font.Font(FONT, 18)

	def award(self,words):
		self.words = words
		self.image = self.font.render("%s" % self.words, 1, [255,255,0])
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([412,35])

	def reset(self):
		self.value = 0
		self.off_screen = 0
		self.colours = [ [255,255,0], [255,128,0], [255,255,0], [255,128,0], [255,255,0], [255,128,0] ]
		self.last_update = 0

	def update(self):
		try:
			time_now = pygame.time.get_ticks()
			if (time_now - self.last_update) >= 125:
				self.last_update = time_now
				colour = self.colours.pop()
				self.image = self.font.render("%s" % self.words, 1, colour)
				self.rect = self.image.get_rect()
				self.rect = self.rect.move([412,35])
		except:
			self.off_screen = 1
			self.colours = [ [255,255,0], [255,128,0], [255,255,0], [255,128,0], [255,255,0], [255,128,0] ]

class Collect(pygame.sprite.Sprite):
	def __init__(self,game):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.colour = [255,255,255]
		self.clicked = 0
		self.last_update = pygame.time.get_ticks()
		self.font = pygame.font.Font(FONT, 22)
		self.image = self.font.render("Collect", 1, self.colour)
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,220])

	def click_test(self):
		x,y = pygame.mouse.get_pos()
		area = pygame.Rect(x,y,1,1)

		if area.colliderect(self.rect):
			self.clicked = 1
		else:
			self.clicked = 0

	def reset(self):
		self.clicked = 0

	def update(self):
		x,y = pygame.mouse.get_pos()
		area = pygame.Rect(x,y,1,1)

		time_now = pygame.time.get_ticks()
		if area.colliderect(self.rect):
			self.colour = [255,0,0]
		elif (time_now - self.last_update) >= 500 and self.game.timer.timer <= 10 and not self.game.timer.time_up():
			self.last_update = time_now
			if self.colour == [255,128,0]:
				self.colour = [255,255,255]
			elif self.colour == [255,255,255]:
				self.colour = [255,128,0]
		else:
			if self.colour == [255,0,0]:
				self.colour = [255,255,255]

		self.image = self.font.render("Collect", 1, self.colour)

class EndGame(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.font = pygame.font.Font(FONT, 22)
		self.image = self.font.render("End Game", 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,330])

	def click_test(self):
		x,y = pygame.mouse.get_pos()
		area = pygame.Rect(x,y,1,1)

		if area.colliderect(self.rect):
			sys.exit()

	def update(self):
		x,y = pygame.mouse.get_pos()
		area = pygame.Rect(x,y,1,1)

		if area.colliderect(self.rect):
			self.image = self.font.render("End Game", 1, (255,0,0))
		else:
			self.image = self.font.render("End Game", 1, (255,255,255))

class GameOver(pygame.sprite.Sprite):
	def __init__(self,game):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.font = pygame.font.Font(FONT, 24)
		self.image = self.font.render("Game Over", 1, (0,0,0))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([150,60])

	def update(self):
		if self.game.game_over == 1:
			self.image = self.font.render("Game Over", 1, (0,0,0))

class HiScore(pygame.sprite.Sprite):
	def __init__(self,game,score,colour,pos):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.score = str(score)
		self.colour = colour
		self.font = pygame.font.Font(FONT, 22)
		self.image = self.font.render(self.score, 1, self.colour)
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(pos)

	def update(self):
		if self.game.game_over == 1:
			self.image = self.font.render(self.score, 1, self.colour)

class NewGame(pygame.sprite.Sprite):
	def __init__(self,game):
		pygame.sprite.Sprite.__init__(self)

		self.game = game
		self.font = pygame.font.Font(FONT, 22)
		self.image = self.font.render("New Game", 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,300])

	def click_test(self):
		x,y = pygame.mouse.get_pos()
		area = pygame.Rect(x,y,1,1)

		if area.colliderect(self.rect):
			self.game.restart()

	def update(self):
		x,y = pygame.mouse.get_pos()
		area = pygame.Rect(x,y,1,1)

		if area.colliderect(self.rect):
			self.image = self.font.render("New Game", 1, (255,0,0))
		else:
			self.image = self.font.render("New Game", 1, (255,255,255))

class SubmitScore(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.score = 0
		self.font = pygame.font.Font(FONT, 22)
		self.image = self.font.render("Submit your score", 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,260])

	def reset(self):
		self.score = 0
		self.rect = self.rect.move([410,260])

	def update(self):
		x,y = pygame.mouse.get_pos()
		area = pygame.Rect(x,y,1,1)

		if area.colliderect(self.rect):
			self.image = self.font.render("Submit your score", 1, (255,0,0))
			if pygame.mouse.get_pressed()[0]:
				webbrowser.open("http://www.playaholics.com/comp_entry.php?game=Slider&developer=playaholics&score=%d" % (self.score))
				self.image = self.font.render("",1,(255,0,0))
				self.rect = self.image.get_rect()
				self.rect = self.rect.move([-100,-100])
		
		else:
			self.image = self.font.render("Submit your score", 1, (255,255,255))

class Timer(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.in_game = 0
		self.time_limit = 60
		self.last_update = 0
		self.timer = self.time_limit

		self.font = pygame.font.Font(FONT, 32)
		self.image = self.font.render("Time: %s" % self.time_limit, 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,55])
		sound_file = os.path.join('sounds', 'tock.wav')
		self.sound = pygame.mixer.Sound(sound_file)
		self.sound.set_volume(0.15)

	def reset(self):
		"""Resets the timer for the next level"""
		self.time_limit = 60
		self.timer = self.time_limit
		self.start_time = int(time.time())
		self.last_update = 0

	def start(self):
		self.in_game = 1
		self.start_time = int(time.time())

	def stop(self):
		self.timer = 0
		self.in_game = 0

	def time_up(self):
		"""Boolean end of level check"""
		if self.timer <= 0:
			return 1
		else:
			return 0

	def update(self):
		time_now = pygame.time.get_ticks()
		if (time_now - self.last_update) >= 1000 and self.in_game:
			self.last_update = time_now
			self.timer = self.timer-1
			self.sound.play()
			self.image = self.font.render("Time: %s" % self.timer, 1, (255,255,255))

class Word(pygame.sprite.Sprite):
	def __init__(self,word,pos):
		pygame.sprite.Sprite.__init__(self)
		
		self.word = word
		self.font = pygame.font.Font(FONT, 22)
		self.colours = [ [255,255,0], [255,128,0], [255,255,0], [255,128,0], [255,255,0], [255,128,0] ]
		self.image = self.font.render(word, 1, [255,255,0])
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(pos)

	def update(self):
		try:
			time_now = pygame.time.get_ticks()
			if (time_now - self.last_update) >= 125:
				self.last_update = time_now
				colour = self.colours.pop()
				self.image = self.font.render(self.word, 1, colour)
				self.rect = self.image.get_rect()
				self.rect = self.rect.move([412,35])
		except:
			self.off_screen = 1

class WordsHeader(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.font = pygame.font.Font(FONT, 22)
		self.image = self.font.render("Find these words:", 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,100])

	def update(self):
		pass