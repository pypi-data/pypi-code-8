from enum import Enum
from collections import deque

TILE_SIZE = 20

WIDTH = TILE_SIZE * 40
HEIGHT = TILE_SIZE * 30


class Direction(Enum):
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    UP = (0, -1)
    DOWN = (0, 1)


class Crashed(Exception):
    """The snake has crashed into itself."""


class Snake:
    def __init__(self, pos=(20, 20)):
        self.pos = pos
        self.dir = Direction.LEFT
        self.length = 3
        self.tail = deque(maxlen=self.length)

    def move(self):
        dx, dy = self.dir.value
        px, py = self.pos
        self.pos = (px + dx, py + dy)
        self.tail.appendleft(self.pos)
        for t in self.tail[1:]:
            if t == self.pos:
                raise Crashed(t)

    def grow(self):
        self.length += 1
        self.tail = deque(self.tail, maxlen=self.length)

    def draw(self):
        for (x, y) in self.tail:
            r = Rect(TILE_SIZE * x, TILE_SIZE * y, TILE_SIZE, TILE_SIZE)
            screen.draw.filled_rect(r, 'green')
