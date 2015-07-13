from gui.shape_ui import ShapeUI
from PyQt5.QtGui import QPixmap


class BulletUI(ShapeUI):
    def __init__(self, parent, game, player_ui):
        super().__init__(parent, game)
        self.player_ui = player_ui
        self.image_height_fix = 5

        self.pixmap = QPixmap("../images/bullet.png")

        self.set_shape_size()

        self.set_initial_position()
        self.show()

    def set_initial_position(self):
        """Set the initial position of the bullet and moves the bullet
        there.
        """
        self.x = self.player_ui.x + self.player_ui.width / 2 - 15
        self.y = self.player_ui.y - self.player_ui.height / 2 + 15

        self.move(self.x, self.y)

        self.update()

    def move_to_target(self):
        """Moves the bullet up (to the tagrget)."""
        self.y -= 5
        self.move(self.x, self.y)
