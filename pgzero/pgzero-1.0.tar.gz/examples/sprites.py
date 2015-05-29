alien = Actor('alien')
WIDTH = alien.width
HEIGHT = alien.height
alien.topleft = 0, 0


def draw():
    screen.clear()
    alien.draw()
