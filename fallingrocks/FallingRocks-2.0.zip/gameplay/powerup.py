from enum import IntEnum
import random


class PowerupType(IntEnum):
    no_powerup = 0
    player_invinciblility = 1
    big_bomb = 2
    slow_down_rocks = 3
    shoot_rocks = 4


class PowerupDuration(IntEnum):
    no_duration = 0
    instant = 10
    small = 10 * 1000
    medium = 15 * 1000
    big = 20 * 1000


class PowerupTimeInterval(IntEnum):
    no_time_interval = 0
    second = 1000
    small = 12413
    medium = 34847
    big = 47093
    very_big = 65239


class Powerup:
    def __init__(self, type):
        self.__type = type
        self.__duration = PowerupDuration.no_duration

    def set_duration(self, powerup_type):
        """Sets the duration of powerup types."""
        if powerup_type == PowerupType.player_invinciblility:
            self.__duration = int(PowerupDuration.medium)
        elif powerup_type == PowerupType.big_bomb:
            self.__duration = int(PowerupDuration.instant)
        elif powerup_type == PowerupType.slow_down_rocks:
            self.__duration = int(PowerupDuration.small)
        elif powerup_type == PowerupType.shoot_rocks:
            self.__duration = int(PowerupDuration.medium)

    def set_random_position(self, max_value):
        """Sets a random number from 10 to max_value which is used for setting
        the position of the powerup.
        """
        return random.randint(10, max_value)

    @property
    def powerup_duration(self):
        """Gets the powerup's duration."""
        return self.__duration
