class Bullet:
    def __init__(self):
        self.__speed = 50

    def set_speed(self, new_speed):
        """Sets the bullet's speed to the value of new_speed."""
        self.__speed = new_speed

    @property
    def bullet_speed(self):
        """Gets the bullet's speed."""
        return self.__speed
