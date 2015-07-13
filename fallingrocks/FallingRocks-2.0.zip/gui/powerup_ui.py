from PyQt5.QtGui import QPixmap
from gui.shape_ui import ShapeUI
from gameplay.powerup import PowerupType


class PowerupUI(ShapeUI):
    def __init__(self, parent, game, type):
        super().__init__(parent, game)
        self.type = type
        self.image_height_fix = 5
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
            self.pixmap = QPixmap("../images/invinciblility.png")
        elif type == PowerupType.big_bomb:
            self.pixmap = QPixmap("../images/big_bomb.png")
        elif type == PowerupType.slow_down_rocks:
            self.pixmap = QPixmap("../images/slow_down_rocks.png")
        elif type == PowerupType.shoot_rocks:
            self.pixmap = QPixmap("../images/shoot_rocks.png")

    def drop_down(self):
        """Moves the powerup down."""
        self.y += 5
        self.move(self.x, self.y)

    def set_duration(self):
        self.powerup.set_duration(self.type)

    @property
    def duration(self):
        return self.powerup.powerup_duration
