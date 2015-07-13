from player import Player
from rock import Rock
from powerup import Powerup, PowerupType
from bullet import Bullet


class Field:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.rocks = []
        self.powerups = []
        self.bullets = []
        self.__player = Player()
        self.__rock = Rock()
        self.__powerup = Powerup(PowerupType.no_powerup)
        self.__bullet = Bullet()

    def set_rock_speed(self, new_speed):
        """Sets the rock's speed to the value of new_speed."""
        self.__rock.set_speed(new_speed)

    @property
    def rock_speed(self):
        """Gets the rock's speed."""
        return self.__rock.rock_speed

    @property
    def player_speed(self):
        """Gets the player's speed."""
        return self.__player.player_speed

    @property
    def bullet_speed(self):
        """Gets the bullet's speed."""
        return self.__bullet.bullet_speed

    @property
    def player(self):
        """Gets the player's object."""
        return self.__player

    @property
    def rock(self):
        """Gets the rock's object."""
        return self.__rock

    @property
    def powerup(self):
        """Gets the powerup's object."""
        return self.__powerup

    @property
    def bullet(self):
        """Gets the bullet's speed."""
        return self.__bullet
