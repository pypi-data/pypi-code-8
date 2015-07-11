from gui.shape_ui import ShapeUI
from PyQt5.QtGui import QPixmap
from powerup import PowerupType


class RockUI(ShapeUI):
    def __init__(self, parent, game):
        super().__init__(parent, game)
        self.rock_shape_number = 8
        self.image_height_fix = 10

        self.rock = self.game.rock
        self.shape = self.rock

        self.set_random_shape()

        self.set_shape_size()

        self.set_random_position()
        self.show()

    def set_random_shape(self):
        """Sets a random shape of the rock."""
        self.random_shape = self.rock.\
            set_random_shape(self.rock_shape_number)
        self.pixmap = QPixmap("images/rock" + str(self.random_shape) + ".png")

    def drop_down(self):
        """Moves the rock down."""
        self.y += 5
        self.move(self.x, self.y)


class PowerupUI(ShapeUI):
    def __init__(self, parent, game, type):
        super().__init__(parent, game)
        self.type = type
        self.image_height_fix = 5
        print(self.type)
        self.powerup = self.game.powerup
        self.shape = self.powerup

        self.set_duration()

        self.set_shape(self.type)

        self.set_shape_size()

        self.set_random_position()
        self.show()

    def set_shape(self, type):
        """Sets the shape of the powerup according to it's type."""
        if type == PowerupType.player_invinciblility:
            self.pixmap = QPixmap("images/invinciblility.png")
        elif type == PowerupType.big_bomb:
            self.pixmap = QPixmap("images/big_bomb.png")
        elif type == PowerupType.slow_down_rocks:
            self.pixmap = QPixmap("images/slow_down_rocks.png")
        elif type == PowerupType.shoot_rocks:
            self.pixmap = QPixmap("images/shoot_rocks.png")

    def drop_down(self):
        """Moves the powerup down."""
        self.y += 5
        self.move(self.x, self.y)

    def set_duration(self):
        print(self.type)
        self.powerup.set_duration(self.type)

    @property
    def duration(self):
        return self.powerup.powerup_duration
