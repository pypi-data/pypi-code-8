import random
from enum import Enum
from collections import deque
from itertools import islice


TILE_SIZE = 24

TILES_W = 20
TILES_H = 15

WIDTH = TILE_SIZE * TILES_W
HEIGHT = TILE_SIZE * TILES_H


def screen_rect(tile_pos):
    """Get the screen rectangle for the given tile coordinate."""
    x, y = tile_pos
    return Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Crashed(Exception):
    """The snake has crashed into itself."""


class Snake:
    def __init__(self, pos=(TILES_W // 2, TILES_H // 2)):
        self.pos = pos
        self.dir = Direction.LEFT
        self.length = 4
        self.tail = deque(maxlen=self.length)

    def move(self):
        dx, dy = self.dir.value
        px, py = self.pos
        px = (px + dx) % TILES_W
        py = (py + dy) % TILES_H

        self.pos = px, py
        self.tail.appendleft(self.pos)
        for t in islice(self.tail, 1, None):
            if t == self.pos:
                raise Crashed(t)

    def __len__(self):
        return self.length

    def __contains__(self, pos):
        return any(p == pos for p in self.tail)

    def grow(self):
        self.length += 1
        self.tail = deque(self.tail, maxlen=self.length)

    def draw(self):
        for pos in self.tail:
            screen.draw.filled_rect(screen_rect(pos), 'green')


class Apple:
    def __init__(self):
        self.pos = 0, 0

    def draw(self):
        screen.blit(images.apple, screen_rect(self.pos))


KEYBINDINGS = {
    keys.LEFT: Direction.LEFT,
    keys.RIGHT: Direction.RIGHT,
    keys.UP: Direction.UP,
    keys.DOWN: Direction.DOWN,
}


snake = Snake()
snake.alive = True

apple = Apple()


def place_apple():
    """Randomly place the apple somewhere that isn't currently occupied.

    We will generate coordinates at random until we find some that are not on
    top of the snake.

    """
    if len(snake) == TILES_W * TILES_H:
        raise ValueError("No empty spaces!")

    while True:
        pos = (
            random.randrange(TILES_W),
            random.randrange(TILES_H)
        )

        if pos not in snake:
            apple.pos = pos
            return


def on_key_down(key):
    dir = KEYBINDINGS.get(key)
    if dir:
        snake.dir = dir
        return


def tick():
    if not snake.alive:
        return

    try:
        snake.move()
    except Crashed:
        snake.alive = False
        stop()
    else:
        if snake.pos == apple.pos:
            snake.grow()
            start()
            place_apple()


def start():
    """Set/update the tick interval.

    This is called whenever the snake grows to make the game run faster.

    """
    interval = max(0.1, 0.6 - 0.05 * (len(snake) - 3))
    clock.unschedule(tick)
    clock.schedule_interval(tick, interval)


def stop():
    """Stop the game from updating."""
    clock.unschedule(tick)


def draw():
    screen.clear()
    snake.draw()
    apple.draw()

    screen.draw.text(
        'Score: %d' % len(snake),
        color='white',
        topright=(WIDTH - 5, 5)
    )

    if not snake.alive:
        screen.draw.text(
            "You died!",
            color='white',
            center=(WIDTH/2, HEIGHT/2)
        )




place_apple()
start()
