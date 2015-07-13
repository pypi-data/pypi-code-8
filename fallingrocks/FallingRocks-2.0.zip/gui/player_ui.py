from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QPixmap
from gui.shape_ui import ShapeUI


class PlayerUI(ShapeUI):
    def __init__(self, parent, game):
        super().__init__(parent, game)
        self.player = game.player
        self.speed = game.player_speed

        self.pixmap = QPixmap("../images/smile.png")
        self.image_height_fix = 48

        self.width = self.pixmap.width()
        self.height = self.pixmap.height()

        self.set_shape_size()

        self.set_initial_position()
        self.show()

    def set_initial_position(self):
        """Set the initial position of the player and moves the player
        there.
        """
        self.x = (self.field_width - self.image_size[0]) / 2
        self.y = self.field_height - 50
        self.move(self.x, self.y)

    @property
    def is_player_invincible(self):
        """Checks if the player is invincible"""
        return self.player.is_player_invincible

    def set_player_invinciblity(self):
        """Sets the player's invincibility to the opposite of the current
        value.
        """
        self.player.set_player_invinciblity()

    @pyqtSlot()
    def move_left(self):
        """Moves the player to the left and checks if the move is valid
        (if the move is out of the game field).
        """
        if(self.x - self.speed > 0):
            self.x -= self.speed
            self.move(self.x, self.y)

    @pyqtSlot()
    def move_right(self):
        """Moves the player to the right and checks if the move is valid
        (if the move is out of the game field).
        """
        if(self.x + self.speed < self.field_width -
           self.image_size[0]):
            self.x += self.speed
            self.move(self.x, self.y)
