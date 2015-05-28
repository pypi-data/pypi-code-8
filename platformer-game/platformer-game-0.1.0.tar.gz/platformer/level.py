from random import random

import pygame

from physics import tilesize
from physics import timeofday
import gradient


class Platform(pygame.sprite.Sprite):
	"""One solid block."""
	def __init__(self, pos, color=(0, 0, 0)):
		super(Platform, self).__init__(self.groups)
		self.image = pygame.Surface((tilesize, tilesize))
		self.image.fill(color)
		self.rect = self.image.get_rect(topleft=pos)


class Level:
	"""A map containing platforms.

	A level typically fills the screen. If the player exits the level in any
	direction she enters the next one.
	"""

	def __init__(self, parent):
		self.parent = parent
		self.map = []
		for y in range(self.parent.height):
			line = []
			for x in range(self.parent.width):
				line.append('.')
			self.map.append(line)

	def load(self):
		"""Generate platforms from map."""
		for y in range(self.parent.height):
			for x in range(self.parent.width):
				if self.map[y][x] != ".":
					Platform((x * tilesize, y * tilesize))

	def get(self, x, y, default=None):
		try:
			return self.map[y][x]
		except IndexError:
			return default

	def to_int(self, x, y):
		a = self.get(x, y)
		if a is None:
			return 0
		elif a == '.':
			return -1
		else:
			return 1

	def __str__(self):
		return '\n'.join([''.join(row) for row in self.map])


class LevelManager:
	"""Generate and store all levels."""

	platforms = pygame.sprite.OrderedUpdates()

	def __init__(self):
		self._dict = dict()
		self.width = 24
		self.height = 12
		self.current = (0, 0)
		self.background = pygame.Surface((self.width * tilesize,
			self.height * tilesize))
		self.load(0, 0)

	def load(self, X, Y):
		"""Load level at position (X, Y)."""

		self.current = (X, Y)

		for sprite in self.platforms.sprites():
			sprite.kill()

		if (X, Y) not in self._dict:
			self.generate(X, Y)

		self._dict[(X, Y)].load()

		# also update gradient (only on level change for performance)
		gradient.draw(self.background, gradient.Background.gradient(timeofday()))

	def generate(self, X, Y):
		"""Generate a random level."""

		level = Level(self)

		x_min = 0
		x_max = self.width - 1
		y_min = 0
		y_max = self.height - 1

		# borders in adjacent levels should be the same
		if (X + 1, Y) in self._dict:
			x_max = self.width - 2
			for y in range(self.height):
				level.map[y][self.width - 1] = self._dict[(X + 1, Y)].map[y][0]

		if (X - 1, Y) in self._dict:
			x_min = 1
			for y in range(self.height):
				level.map[y][0] = self._dict[(X - 1, Y)].map[y][self.width - 1]

		if (X, Y + 1) in self._dict:
			y_max = self.height - 2
			for x in range(self.width):
				level.map[self.height - 1][x] = self._dict[(X, Y + 1)].map[0][x]

		if (X, Y - 1) in self._dict:
			y_min = 1
			for x in range(self.width):
				level.map[0][x] = self._dict[(X, Y - 1)].map[self.height - 1][x]

		def field(x, y, f=2, r=1.5, threshold=0):
				A = [
					level.to_int(x, y - 1),
					level.to_int(x, y + 1),
					level.to_int(x + 1, y),
					level.to_int(x - 1, y)]

				B = [
					level.to_int(x - 1, y - 1),
					level.to_int(x + 1, y - 1),
					level.to_int(x - 1, y + 1),
					level.to_int(x + 1, y + 1)]

				a = sum(A) * 1.0 / sum([abs(xx) for xx in A])
				b = sum(B) * 1.0 / sum([abs(xx) for xx in B])

				c = f * a - b
				d = 2 * r * random() - r

				return 'X' if c + d > threshold else '.'

		while x_min <= x_max and y_min <= y_max:
			for x in range(x_min, x_max + 1):
				level.map[y_min][x] = field(x, y_min)
			y_min += 1

			for y in range(y_min, y_max + 1):
				level.map[y][x_min] = field(x_min, y)
			x_min += 1

		self._dict[(X, Y)] = level

	# load() shortcuts
	def right(self):
		"""Load the level right of the current one."""
		X, Y = self.current
		self.load(X + 1, Y)

	def left(self):
		"""Load the level left of the current one."""
		X, Y = self.current
		self.load(X - 1, Y)

	def up(self):
		"""Load the level above the current one."""
		X, Y = self.current
		self.load(X, Y - 1)

	def down(self):
		"""Load the level below the current one."""
		X, Y = self.current
		self.load(X, Y + 1)
