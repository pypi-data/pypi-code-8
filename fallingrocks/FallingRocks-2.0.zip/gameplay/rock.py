import random


class Rock:
    def __init__(self):
        self.__speed = 50

    def set_random_position(self, max_value):
        """Sets a random number from 10 to max_value which is used for setting
        the position of the rock.
        """
        return random.randint(10, max_value)

    def set_random_shape(self, max_value):
        """Sets a random number from 1 to max_value which is used for setting
        the shape of the rock.
        """
        return random.randint(1, max_value)

    def set_speed(self, new_speed):
        """Sets the rock's speed to the value of new_speed."""
        self.__speed = new_speed

    @property
    def rock_speed(self):
        """Gets the rock's speed."""
        return self.__speed
