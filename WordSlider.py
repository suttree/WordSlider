#! /usr/bin/env python

import os
import re
import sys
import string
import random
import pygame
import marshal
import webbrowser

from pygame.locals import *
from menu.Hints import HintHeader, HintLine1, HintLine2
from menu.Items import Bonus, Collect, EndGame, GameOver, HiScore, NewGame, SubmitScore, Timer, Word, WordsHeader

FONT = os.path.join('fonts', 'nrkis.ttf')

class Game:
	def __init__(self):
		self.game_over = 0

		self.prev_x = 0
		self.prev_y = 0
		self.last_click = 0

		file = open(os.path.join('wordlists','simple.txt'), 'r')
		self.wordlist = file.readlines()
		
		for i in range(len(self.wordlist)):
			self.wordlist[i] = string.replace(self.wordlist[i], "\n", "")

		self.hi_scores = []
		self.load_scores()

	def create_grid(self):
		# This is the grid, remove 4 squares and then create it
		positions = [
			'0,0',   '50,0',   '100,0',   '150,0',   '200,0',   '250,0',   '300,0',   '350,0',
			'0,50',  '50,50',  '100,50',  '150,50',  '200,50',  '250,50',  '300,50',  '350,50',
			'0,100', '50,100', '100,100', '150,100', '200,100', '250,100', '300,100', '350,100',
			'0,150', '50,150', '100,150', '150,150', '200,150', '250,150', '300,150', '350,150',
			'0,200', '50,200', '100,200', '150,200', '200,200', '250,200', '300,200', '350,200',
			'0,250', '50,250', '100,250', '150,250', '200,250', '250,250', '300,250', '350,250',
			'0,300', '50,300', '100,300', '150,300', '200,300', '250,300', '300,300', '350,300',
			'0,350', '50,350', '100,350', '150,350', '200,350', '250,350', '300,350', '350,350',
		]

		random.shuffle(positions)

		positions.pop()
		positions.pop()
		positions.pop()
		positions.pop()
		positions.pop()
		positions.pop()
		positions.pop()
		positions.pop()

		for i in range(2):
			for word in self.target_words:
				for letter in word:
					x,y = positions.pop().split(',')
					self.tiles.add(Tile( letter, [int(x),int(y)] ))

		for pos in positions:
			x,y = pos.split(',')
			self.tiles.add(Tile( self.letters[ random.randrange(len(self.letters)) ], [int(x),int(y)] ))

	def demo_mode(self):
		pygame.init()

		pygame.display.set_caption('Playaholics: WordSlider')
		self.screen = pygame.display.set_mode([600,400])
		self.background = pygame.image.load('images/how_to_play.png').convert()
		self.screen.blit(self.background, [0, 0])
		pygame.display.update()

		sound_file = os.path.join('sounds', 'dink.wav')
		self.sound = pygame.mixer.Sound(sound_file)

		sound_file = os.path.join('sounds', 'wah.wav')
		self.soundtrack = pygame.mixer.Sound(sound_file)
		self.soundtrack.set_volume(0.6)
		self.soundtrack.play(-1)

		sound_file = os.path.join('sounds', 'bonus.wav')
		self.bonus_sound = pygame.mixer.Sound(sound_file)
		self.bonus_sound.set_volume(0.5)

		sound_file = os.path.join('sounds', 'buzzer.wav')
		self.penalty_sound = pygame.mixer.Sound(sound_file)
		self.penalty_sound.set_volume(0.5)

		sound_file = os.path.join('sounds', 'bonus.wav')
		self.game_over_sound = pygame.mixer.Sound(sound_file)
		self.game_over_sound.set_volume(0.5)

		in_demo=1
		while in_demo:
			for event in pygame.event.get():
				if event.type == QUIT:
					#webbrowser.open("http://www.playaholics.com/")
					sys.exit()

				elif event.type == MOUSEBUTTONDOWN:
					in_demo=0
					self.soundtrack.fadeout(10000)
				else:
					pass

		self.start()

	def double_clicked(self,x,y):
		time_now = pygame.time.get_ticks()
		pause = time_now - self.last_click
	
		if self.prev_x == x and self.prev_y == y:
			if pause <= 300:
				return 1
	
		self.prev_x     = x
		self.prev_y     = y
		self.last_click = time_now

		return 0

	def load_scores(self):
		self.top_scores = []
		try:
			scores = os.path.join('menu', 'scores.dat')
			infile = open(scores, "rb")
			self.top_scores = marshal.load(infile)
			infile.close()
		except:
			pass

	def remove_tile(self,pos):
		"""Remove each processed tile from the board at the end of a round"""
		self.marker.rect[0] = pos[0]
		self.marker.rect[1] = pos[1]
		rectlist = pygame.sprite.spritecollide(self.marker,self.tiles,1)
		self.sound.play()
		pygame.display.update(rectlist)
		pygame.time.wait(50)

	def pick_words(self):
		self.target_words = []
		for i in range(4):
			self.target_words.append(self.wordlist[random.randrange(len(self.wordlist))])

		self.words_to_find = []
		self.words_to_find.append(Word(self.target_words[0],[410,125]))
		self.words_to_find.append(Word(self.target_words[1],[410,145]))
		self.words_to_find.append(Word(self.target_words[2],[410,165]))
		self.words_to_find.append(Word(self.target_words[3],[410,185]))

		for word in self.words_to_find:
			self.gamesprites.add(word)

	def reset(self):
		self.game_over = 0
		self.bonus.reset()

		self.gamesprites.remove(self.bonus)

		for word in self.words_to_find:
			self.gamesprites.remove(word)

	def restart(self):
		"""Restart the game"""

		self.tiles.empty()

		self.reset()
		self.timer.reset()
		self.score.reset()
		self.submit_score_menu.reset()

		for hi_score in self.hi_scores:
			self.menusprites.remove(hi_score)

		self.gamesprites.remove(self.bonus)
		self.menusprites.remove(self.game_over_menu)
		self.menusprites.remove(self.submit_score_menu)

		self.letters = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' ]

		self.run()

	def run(self):
		"""Run the game"""

		self.timer.start()
		self.pick_words()
		self.create_grid()
		self.score.calculate(self.tiles, self.target_words)	# do this now to highlight any words that are already present (yuk!)

		# Restrict what events we have to deal with
		pygame.event.set_allowed(None)
		pygame.event.set_allowed([QUIT,MOUSEBUTTONDOWN,MOUSEMOTION,MOUSEBUTTONUP])
		
		# Animate the tiles, scores and timers
		start_tile = None
		end_tile = None
		moveable = 1
		moved = False
		while 1:
			for event in pygame.event.get():
				if event.type == QUIT:
					#webbrowser.open("http://www.playaholics.com")
					sys.exit()

				elif event.type == MOUSEBUTTONDOWN:
					moved = False
					moveable = 1
					x,y = pygame.mouse.get_pos()
					starting_clicked_area = pygame.Rect(x,y,1,1)
		
					# Have we clicked on a tile rather than a space?
					for tile in self.tiles.sprites():
						if starting_clicked_area.colliderect(tile.rect):
							start_tile = tile

					# If we've double clicked on a tile, then attempt
					# to move in in this order - up, down, left, right
					if self.double_clicked(x,y) and start_tile:
						for direction in ['up','down','left','right']:
							if not moveable:
								break
							if direction == 'up':
								neighbour_x = start_tile.rect[0]
								neighbour_y = start_tile.rect[1]-50
							elif direction == 'down':
								neighbour_x = start_tile.rect[0]
								neighbour_y = start_tile.rect[1]+50
							elif direction == 'left':
								neighbour_x = start_tile.rect[0]-50
								neighbour_y = start_tile.rect[1]
							elif direction == 'right':
								neighbour_x = start_tile.rect[0]+50
								neighbour_y = start_tile.rect[1]

							if neighbour_x < 0 or neighbour_y < 0:
								continue
							elif neighbour_x > 350 or neighbour_y > 350:
								continue

							neighbour = pygame.Rect(neighbour_x,neighbour_y,1,1)

							for tile in self.tiles.sprites():
								if neighbour.colliderect(tile.rect):
									end_tile = tile

							if not end_tile:
								moveable = 0
								start_tile.move([neighbour_x,neighbour_y])
		
							end_tile = None

 				elif event.type == MOUSEMOTION:
					try:
						if moveable:
							x,y = pygame.mouse.get_pos()
							if x < 0:
								x=0
							if x > 350:
								x=350
							if y < 0:
								y=0
							if y > 350:
								y=350
							finishing_dragged_area = pygame.Rect(x,y,10,10)
			
							# Are we over a tile? If so, we can't slide here
							for tile in self.tiles.sprites():
								if finishing_dragged_area.colliderect(tile.rect):
									end_tile = tile
									break

							# Move unless we're tile skipping
							if x > start_tile.rect[0]+75:
								pass
							elif y > start_tile.rect[1]+75:
								pass
							elif start_tile.fixed:
								pass
							elif start_tile and not end_tile:
								start_tile.move([x,y])
								moved = True

							end_tile = None
					except:
						pass

				elif event.type == MOUSEBUTTONUP:
					# See if we've got a word in the grid now that the tile has stopped moving
					if moved:
						x,y = pygame.mouse.get_pos()
						self.found_words = self.score.calculate(self.tiles, self.target_words,0)

					self.collect.click_test()
					self.end_game.click_test()
					self.new_game.click_test()

					start_tile = None
					end_tile = None
					moveable = 0

			self.tiles.update()
			self.score.update()
			self.gamesprites.update()
			self.menusprites.update()

			if self.bonus.off_screen:
				self.bonus.reset()
				self.gamesprites.remove(self.bonus)

			if self.collect.clicked and not self.game_over:
				self.found_words = self.score.calculate(self.tiles, self.target_words)

				for word in self.found_words:
					self.timer.timer = self.timer.timer + len(word) * 2 * len(self.found_words)

				words = ", ".join(self.found_words)

				if len(words) > 0:
					self.bonus.award(words)
					self.gamesprites.add(self.bonus)
				else:
					self.bonus.award("-5 seconds!")
					self.gamesprites.add(self.bonus)

				if self.timer.timer > 60:
					self.timer.timer = 60

				for sprite in self.tiles.sprites():
					self.remove_tile(sprite.rect)

				for word in self.words_to_find:
					self.gamesprites.remove(word)

				for i in range(len(self.found_words)):
					self.bonus_sound.play()

				if not self.found_words:
					self.penalty_sound.play()
					self.timer.timer = self.timer.timer - 5

				self.collect.clicked = 0

				self.pick_words()
				self.create_grid()
				self.score.calculate(self.tiles, self.target_words)

			if self.timer.time_up():
				self.timer.stop()

				for sprite in self.tiles.sprites():
					self.remove_tile(sprite.rect)

				self.submit_score_menu.score = self.score.score

				if not self.game_over:
					self.save_scores()

					i = 0
					colour = ""
					self.hi_scores = []
					self.hi_scores.append(HiScore(self,"Hi-Scores",[255,255,255],[150,90]))
					for score in self.top_scores:
						i = i + 1

						if score == self.score.score:
							colour = [255,0,0]
						else:
							colour = [0,0,0]

						if i < 10:
							score = " %d.    %d" % (i, score)
						else:
							score = "%d.   %d" % (i, score)

						self.hi_scores.append(HiScore(self,score,colour,[150,100+20*i]))

					for hi_score in self.hi_scores:
						self.menusprites.add(hi_score)

					self.game_over_sound.play()

				self.game_over = 1

			if not self.game_over:
				tile_list = self.tiles.draw(self.screen)
				pygame.display.update(tile_list)

			ui_list = self.gamesprites.draw(self.screen)
			pygame.display.update(ui_list)
			menu_list = self.menusprites.draw(self.screen)
			pygame.display.update(menu_list)

			pygame.time.delay(10)
			self.tiles.clear(self.screen, self.background)
			self.gamesprites.clear(self.screen, self.background)
			self.menusprites.clear(self.screen, self.background)

	def save_scores(self):
		if self.score.score not in self.top_scores:
			self.top_scores.append(self.score.score)
		self.top_scores.sort()
		self.top_scores.reverse()
		scores = os.path.join('menu', 'scores.dat')
		outfile = open(scores, "wb")
		marshal.dump(self.top_scores[0:9],outfile)
		outfile.close()

	def start(self):
		"""Initialise the game and start it running"""
		self.screen = pygame.display.set_mode([600,400])
		self.background = pygame.image.load(os.path.join('images','background.png')).convert()
		self.screen.blit(self.background, [0, 0])
		pygame.display.update()

		self.marker = Tile('a',[0,0])

		self.bonus = Bonus()
		self.score = Score()
		self.timer = Timer()
		self.collect = Collect(self)

		self.end_game = EndGame()
		self.new_game = NewGame(self)
		self.words_header = WordsHeader()
		self.game_over_menu = GameOver(self)
		self.submit_score_menu = SubmitScore()

		self.tiles = pygame.sprite.RenderUpdates()
		self.gamesprites = pygame.sprite.RenderUpdates()
		self.menusprites = pygame.sprite.RenderUpdates()
		self.letters = [ 'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z' ]

		self.gamesprites.add(self.score)
		self.gamesprites.add(self.timer)
		self.gamesprites.add(self.words_header)

		self.menusprites.add(self.collect)
		self.menusprites.add(self.end_game)
		self.menusprites.add(self.new_game)

		self.run()

class Score(pygame.sprite.Sprite):
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)

		self.score = 0
		self.tile_groups = {}

		self.font = pygame.font.Font(FONT, 32)
		self.image = self.font.render("Score: %d" % self.score, 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,5])

	def calculate(self,board,targets,award_score=1):
		all_words = []
		found_words = []
		self.word_tiles = []
		self.found_tiles = {}

		self.board = board
		self.targets = targets
		self.time_bonus = 0

		# Left to right, right to left
		all_words.append(self.traverse_grid(0,351,50))
		all_words.append(self.traverse_grid(350,-1,-50))
		# Up and down, down and up
		all_words.append(self.traverse_grid(0,351,50,1))
		all_words.append(self.traverse_grid(350,-1,-50,1))

		regexes = []
		for target in self.targets:
			regexes.append(re.compile(target))

		length = 0
		tmp_word = False
		for words in all_words:
			for word in words:
				if not word:
					continue
				for regex in regexes:
					match = regex.search(word)
					if match:
						# match.group() contains the found word
						if match.group() not in found_words and match.group() != "":
							found_words.append(match.group())

							# Now, we should be able to match up the letters of the found word
							# with the tiles of the found word, then change the tiles and freeze them
							tmp_word = match.group() 
							pos = word.find(tmp_word)
							length = len(tmp_word)

							for i in range(length):
								rect = self.found_tiles[word][pos+i].rect
								self.found_tiles[word][pos+i].image = pygame.image.load('images/found/%s.png' % self.found_tiles[word][pos+i].letter).convert()
								self.found_tiles[word][pos+i].fixed = True

							if award_score:
								self.score = self.score+(len(word)*10)

		return found_words

	def reset(self):
		self.score = 0

	def traverse_grid(self,row,column,step,vertical=0):
		# Keep track of the last tile so that we can
		# check for spaces as word boundaries
		if vertical:
			prev_x = column
			prev_y = row
		else:
			prev_x = row
			prev_y = column

		tile = None
		found_words = []
		for y in range(row,column,step):
			word = []
			tiles = []
			for x in range(row,column,step):
				if vertical:
					current_tile = pygame.Rect(y,x,1,1)
				else:
					current_tile = pygame.Rect(x,y,1,1)

				# Cycle through the tiles and create mostly nonsense strings
				# in each direction. Use those strings as keys to a hash of tiles,
				# so that we can tie up the words to tile positions later on (in calculate)
				for sprite in self.board.sprites():
					if current_tile.colliderect(sprite.rect):
						tile = sprite
						if x > (prev_x+50) or y > (prev_y+50):
							found_words.append("".join(word))
							self.found_tiles["".join(word)] = tiles
							word = []
							tiles = []
							word.append(tile.letter)
							tiles.append(tile)
						elif x < (prev_x-50) or y < (prev_y-50):
							found_words.append("".join(word))
							self.found_tiles["".join(word)] = tiles
							word = []
							tiles = []
							word.append(tile.letter)
							tiles.append(tile)
						else:
							word.append(tile.letter)
							tiles.append(tile)
						prev_x = x
						prev_y = y
			found_words.append("".join(word))
			self.found_tiles["".join(word)] = tiles

		return found_words

	def update(self):
		self.image = self.font.render("Score: %d" % self.score, 1, (255,255,255))
		self.rect = self.image.get_rect()
		self.rect = self.rect.move([410,5])

class Tile(pygame.sprite.Sprite):
	def __init__(self,letter,pos):
		"""Initialise a tile - the basic game unit"""
		pygame.sprite.Sprite.__init__(self)

		self.fixed = False
		self.letter = letter
		self.image = pygame.image.load('images/letters/%s.png' % letter).convert()
		self.rect = self.image.get_rect()
		self.rect = self.rect.move(pos)

	def move(self,pos):
		"""Only move the square if it is a direct neighbour of a blank space"""

		x = pos[0] - (pos[0] % 50)
		y = pos[1] - (pos[1] % 50)

		if x > self.rect[0] or y > self.rect[1]:
			if x > self.rect[0] + 50 or y > self.rect[1] + 50:
				return None

		if x < self.rect[0] or y < self.rect[1]:
			if x < self.rect[0] - 50 or y < self.rect[1] - 50:
				return None

		# Diagonal movements not allowed
		if ( x > self.rect[0] and y > self.rect[1] ) or ( x < self.rect[0] and y < self.rect[1] ):
			return None

		if ( x > self.rect[0] and y < self.rect[1] ) or ( x < self.rect[0] and y > self.rect[1] ):
			return None

		self.rect[0] = x
		self.rect[1] = y

if __name__ == '__main__':
	Game = Game()
	Game.demo_mode()