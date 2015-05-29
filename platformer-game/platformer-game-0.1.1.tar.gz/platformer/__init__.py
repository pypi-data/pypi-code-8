#!/usr/bin/env python

import pygame
from pygame.locals import QUIT, KEYDOWN, K_ESCAPE

from physics import tilesize, framerate
from level import LevelManager, Platform
from player import Player


def main():
	pygame.init()

	savegame = None

	sprites = pygame.sprite.OrderedUpdates()
	Player.groups = sprites,
	Platform.groups = sprites, LevelManager.platforms
	Player.collision_sprites = LevelManager.platforms

	level_manager = LevelManager()
	pygame.display.set_caption("Platformer Demo")
	screen = pygame.display.set_mode((level_manager.width * tilesize,
		level_manager.height * tilesize))

	# initiate objects
	player = Player()
	clock = pygame.time.Clock()

	while 1:
		clock.tick(framerate)
		sprites.update()

		# check for level change
		if player.rect.right > level_manager.width * tilesize:
			level_manager.right()
			player.rect.left = 0
		elif player.rect.left < 0:
			level_manager.left()
			player.rect.right = level_manager.width * tilesize
		elif player.rect.top < 0:
			level_manager.up()
			player.rect.bottom = level_manager.height * tilesize
		elif player.rect.bottom > level_manager.height * tilesize:
			level_manager.down()
			player.rect.top = 0

		for ev in pygame.event.get():
			if ev.type == QUIT:
				pygame.quit()
				return
			if ev.type == KEYDOWN:
				if ev.key == K_ESCAPE:
					pygame.quit()
					return
				elif ev.key == ord('s'):
					# save
					savegame = dict()
					savegame['pos'] = player.rect.x, player.rect.y
					savegame['level'] = level_manager.current
				elif ev.key == ord('l'):
					# load
					if savegame is None:
						raise Exception("no savegame available")
					else:
						level_manager.load(*savegame['level'])
						player.rect.x, player.rect.y = savegame['pos']
			player.handle_event(ev)

		# draw background
		screen.blit(level_manager.background, (0, 0))

		sprites.draw(screen)
		pygame.display.flip()


if __name__ == "__main__":
	main()
