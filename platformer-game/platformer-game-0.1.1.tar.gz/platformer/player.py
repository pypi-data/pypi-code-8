import os
import math

import pygame
from pygame.locals import KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT, K_SPACE
from pygame.locals import Rect

from physics import tilesize, framerate, air_resistance, gravity

LEFT = 0
RIGHT = 1

STAND = 0
WALK = 1
JUMP = 3
HANG = 4
CLIMB = 5


class Player(pygame.sprite.Sprite):
	def __init__(self):
		super(Player, self).__init__(self.groups)

		self.animation_duration = 0.1 * framerate
		self.jump_speed = 11.0 * tilesize / framerate
		self.speed = 3.0 * tilesize / framerate

		p = lambda s: os.path.join(os.path.dirname(__file__), s)
		self.img_default = pygame.image.load(p('sprites/heroine/default.png'))
		self.img_walk = pygame.image.load(p('sprites/heroine/walk.png'))
		self.img_fall = pygame.image.load(p('sprites/heroine/fall.png'))
		self.img_wall_1 = pygame.image.load(p('sprites/heroine/wall_1.png'))
		self.img_wall_2 = pygame.image.load(p('sprites/heroine/wall_2.png'))

		self.x_speed = 0
		self.y_speed = 0
		self.face = RIGHT
		self._animation_tick = 0
		self.set_animation(self.img_default)
		self.state = STAND

		# start position
		self.rect = self.image.get_rect(topleft=[5 * tilesize, 10 * tilesize])

	@property
	def image(self):
		return self.animation[0]

	def set_state(self, key):
		old_state = self.state

		if self.is_jumping():
			self.state = JUMP
		elif self.is_climbing():
			if key[K_UP]:
				self.state = CLIMB
			else:
				self.state = HANG
		else:
			if key[K_LEFT] or key[K_RIGHT]:
				self.state = WALK
			else:
				self.state = STAND

		return self.state != old_state

	def update(self):
		key = pygame.key.get_pressed()

		if self.is_climbing():
			if key[K_UP]:
				self.y_speed = -self.speed
			elif key[K_DOWN]:
				self.y_speed = self.speed + gravity * framerate / 20
			else:
				self.y_speed = gravity * framerate / 20

		if key[K_LEFT]:
			self.x_speed = -self.speed
			self.face = LEFT
		elif key[K_RIGHT]:
			self.x_speed = self.speed
			self.face = RIGHT
		else:
			self.x_speed = 0

		self.x_speed *= 1 - air_resistance
		self.y_speed *= 1 - air_resistance

		if self.is_jumping():
			self.y_speed += gravity

		if self.set_state(key):
			self.select_animation(self.state)
		self.do_animation()
		self.move(self.x_speed, self.y_speed)

	def set_animation(self, *animation):
		if self.face == RIGHT:
			self.animation = list(animation)
		else:
			flip = lambda i: pygame.transform.flip(i, True, False)
			self.animation = [flip(i) for i in animation]

	def do_animation(self):
		self._animation_tick += 1
		if self._animation_tick > self.animation_duration:
			self.animation.append(self.animation.pop(0))
			self._animation_tick = 0

	def select_animation(self, state):
		if state == STAND:
			self.set_animation(self.img_default)
		elif state == WALK:
			self.set_animation(self.img_default, self.img_walk)
		elif state == JUMP:
			self.set_animation(self.img_fall)
		elif state == HANG:
			self.set_animation(self.img_wall_1)
		elif state == CLIMB:
			self.set_animation(self.img_wall_1, self.img_wall_2)

	def is_climbing(self):
		if self.y_speed < -self.speed:
			return False

		new_rect = Rect(self.rect)
		new_rect.width += 2
		new_rect.x -= 1

		for sprite in self.collision_sprites:
			if new_rect.colliderect(sprite.rect):
				self.face = RIGHT if sprite.rect.x > new_rect.x else LEFT
				return True
		return False

	def is_jumping(self):
		if self.is_climbing():
			return False
		else:
			new_rect = Rect(self.rect)
			new_rect.y += 1

			for sprite in self.collision_sprites:
				if new_rect.colliderect(sprite.rect):
					return False
			return True

	def handle_event(self, ev):
		if ev.type == KEYDOWN:
			if ev.key == K_SPACE and not self.is_jumping():
				self.y_speed = -self.jump_speed

	def _move_x(self, dx):
		# Create a temporary new rect that has been moved by dx
		# and check for collisions

		new_rect = Rect(self.rect)
		new_rect.x += dx

		for sprite in self.collision_sprites:
			if new_rect.colliderect(sprite.rect):
				if dx > 0:  # moving right
					return sprite.rect.left - self.rect.right
				else:  # moving left
					return sprite.rect.right - self.rect.left

		return dx

	def _move_y(self, dy):
		# Create a temporary new rect that has been moved by dy
		# and check for collisions

		new_rect = Rect(self.rect)
		new_rect.y += dy

		for sprite in self.collision_sprites:
			if new_rect.colliderect(sprite.rect):
				if dy > 0:  # moving down
					# Landed!
					self.y_speed = 0
					return sprite.rect.top - self.rect.bottom
				elif dy < 0:  # moving up
					# oww, we hit our head
					self.y_speed = 0
					return sprite.rect.bottom - self.rect.top

		return dy

	def move(self, dx, dy):
		self.rect.x += self._move_x(_ceil(dx))
		self.rect.y += self._move_y(_ceil(dy))


def _ceil(x):
	"""
	>>> _ceil(1.5)
	2.0
	>>> _ceil(-1.5)
	-2.0
	"""
	return math.ceil(x) if x > 0 else math.floor(x)
