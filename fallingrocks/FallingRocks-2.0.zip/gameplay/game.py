from enum import Enum
from math import sqrt


class State(Enum):
    running = "running"
    won = "won"
    lost = "lost"
    paused = "paused"
    quit = "quit"


class Game:
    def __init__(self, field):
        self.field = field
        self.init_game_variables()

    def init_game_variables(self):
        self.__state = State.running
        self.__game_speed = 630
        self.__level_speed = 30000
        self.__level = 1

    @property
    def dimensions(self):
        """Gets the dimensions of the game - width and height."""
        return (self.field.width, self.field.height)

    @property
    def is_lost(self):
        """Checks if the game is lost."""
        return self.__state is State.lost

    @property
    def is_won(self):
        """Checks if the game is won."""
        return self.__state is State.won

    @property
    def is_paused(self):
        """Checks if the game is paused."""
        return self.__state is State.paused

    @property
    def is_running(self):
        """Checks if the game is running."""
        return self.__state is State.running

    def lose(self):
        """Loses the game."""
        self.__state = State.lost

    def win(self):
        """Wins the game."""
        self.__state = State.won

    def pause(self):
        """Sets the game's state to paused."""
        self.__state = State.paused

    def resume(self):
        """Sets the game's state to running."""
        self.__state = State.running

    def set_speed(self, new_speed):
        """Sets the game's speed to the value of new_speed."""
        self.__game_speed = new_speed

    def level_up(self):
        """Increments the level of the game."""
        self.__level += 1

    def collision_detected(self, object1, object2):
        """Checks for a collision between object1 and object2."""
        dx = (object1.x + object1.width / 2) - (object2.x + object2.width / 2)
        dy = (object1.y + object1.height / 2) -\
            (object2.y + object2.height / 2)
        distance = sqrt(dx * dx + dy * dy)
        return distance < (object1.width + object2.width) / 2 - 4 or \
            distance < (object1.height + object2.height) / 2 - 8

    @property
    def game_speed(self):
        """Gets the game's speed."""
        return self.__game_speed

    @property
    def rock_speed(self):
        """Gets the rock's speed."""
        return self.field.rock_speed

    @property
    def player_speed(self):
        """Gets the player's speed."""
        return self.field.player_speed

    @property
    def level_speed(self):
        """Gets the level's speed."""
        return self.__level_speed

    @property
    def bullet_speed(self):
        """Gets the bullet's speed."""
        return self.field.bullet_speed

    @property
    def level(self):
        """Gets the current level of the game."""
        return self.__level

    def set_rock_speed(self, new_speed):
        """Gets the rock's speed."""
        self.field.set_rock_speed(new_speed)

    @property
    def rock(self):
        """Gets the rock's object."""
        return self.field.rock

    @property
    def player(self):
        """Gets the player's object."""
        return self.field.player

    @property
    def powerup(self):
        """Gets the powerup's object."""
        return self.field.powerup

    @property
    def bullet(self):
        """Gets the bullet's object."""
        return self.field.bullet

    @property
    def powerups(self):
        """Gets the powerups on the game field."""
        return self.field.powerups

    @property
    def rocks(self):
        """Gets the rocks on the game field."""
        return self.field.rocks

    @property
    def bullets(self):
        """Gets the bullets on the game field."""
        return self.field.bullets

    def reset_game_values(self):
        """Resets the speed of the game, level and rocks and sets the level to
        1.
        """
        self.init_game_variables()
        self.field.set_rock_speed(50)

    def set_speed_after_levelup(self):
        self.set_rock_speed(self.rock_speed - 2)
        self.set_speed(self.game_speed - 27)
