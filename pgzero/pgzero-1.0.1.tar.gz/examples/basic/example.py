alien = Actor('alien')


def draw():
    screen.clear()
    alien.draw()


def update(dt):
    alien.x += 2


def on_mouse_down(button, pos):
    print("Button", button, "pressed")
    sounds.eep.play()
