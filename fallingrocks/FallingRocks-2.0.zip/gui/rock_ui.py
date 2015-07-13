from gui.shape_ui import ShapeUI
from PyQt5.QtGui import QPixmap


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
        self.pixmap = QPixmap("../images/rock" + str(self.random_shape) +
                              ".png")

    def drop_down(self):
        """Moves the rock down."""
        self.y += 5
        self.move(self.x, self.y)
