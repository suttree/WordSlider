#! /usr/bin/env python

import os
import pygame
from pygame.locals import *

FONT = os.path.join('fonts', 'nrkis.ttf')

class HintHeader(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		self.level = 1
		self.font = pygame.font.Font(FONT, 22)
		self.image = self.font.render("How to play:", 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,105])

	def update(self):
		pass

class HintLine1(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.hint = 0
		self.font = pygame.font.Font(FONT, 16)
		self.hint_text = { 0:"Group together 3 or more", 1:"Go edge to edge for", 2:"Clear all the tiles of one", 3:"Earn time for each chain", 4:"You can only earn up" }
		self.image = self.font.render("%s" % self.hint_text[self.hint], 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,130])

	def next(self):
		self.hint = self.hint+1
		try:
			self.image = self.font.render("%s" % self.hint_text[self.hint], 1, (255,255,255))
		except:
			self.hint = 0
			self.image = self.font.render("%s" % self.hint_text[self.hint], 1, (255,255,255))

	def reset(self):
		self.level = 1

	def update(self):
		pass

class HintLine2(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		
		self.hint = 0
		self.font = pygame.font.Font(FONT, 16)
		self.hint_text = { 0:"tiles to score", 1:"an extra bonus", 2:"colour for a 500 point bonus", 3:"cleared from the board", 4:"to 60 seconds of time" }
		self.image = self.font.render("%s" % self.hint_text[self.hint], 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,145])

	def next(self):
		self.hint = self.hint+1
		try:
			self.image = self.font.render("%s" % self.hint_text[self.hint], 1, (255,255,255))
		except:
			self.hint = 0
			self.image = self.font.render("%s" % self.hint_text[self.hint], 1, (255,255,255))

	def reset(self):
		self.level = 1

	def update(self):
		pass