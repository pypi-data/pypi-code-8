from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QLabel


class ShapeUI(QWidget):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.game = game
        self.main_window = parent
        self.image_height_fix = 0
        self.shape = None

        self.field_width = self.game.dimensions[0]
        self.field_height = self.game.dimensions[1]

    def set_shape_size(self):
        """Set the size of the shape to be the same size as the it's image."""
        self.label = QLabel(self)
        self.myScaledPixmap = self.pixmap.scaled(self.label.size(),
                                                 Qt.KeepAspectRatio)
        self.label.setPixmap(self.myScaledPixmap)
        self.image_size = (self.pixmap.width(), self.pixmap.height())
        self.width = self.pixmap.width()
        self.height = self.pixmap.height()

        self.label.setFixedHeight(self.image_size[1] - self.image_height_fix)
        self.label.setFixedWidth(self.image_size[0])
        self.label.setScaledContents(True)

    def set_random_position(self):
        """Sets a random position of the shape and moves the shape there."""
        self.random_coords = self.shape.\
            set_random_position(self.field_width - 15)

        self.x = self.random_coords + 1
        self.y = 1

        self.move(self.x, self.y)
        self.update()

    def remove_shape(self):
        """Removes the shape from the field and destroys the shape object."""
        self.hide()
        self.destroy()
