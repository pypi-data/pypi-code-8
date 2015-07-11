import subprocess
from PyQt5.QtCore import Qt, QBasicTimer, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QFrame, \
    QDesktopWidget
from PyQt5.QtGui import QIcon, QPalette
from powerup import PowerupType, PowerupTimeInterval
from gui.rock_ui import RockUI
from gui.bullet_ui import BulletUI
from gui.powerup_ui import PowerupUI
from gui.player_ui import PlayerUI
from gui.communicate import Communicate


class UserInterface:
    def __init__(self, game):
        self.game = game

    def main_loop(self):
        """Initializes the app and the main window of the game and starts the
        main loop of the game.
        """
        UserInterface.app = QApplication([])
        UserInterface.main_window = MainWindow(self.game)
        UserInterface.app.exec_()

    @staticmethod
    def close_app():
        """Exits the game and closes the game application."""
        UserInterface.app.exit()

    @staticmethod
    def get_main_window():
        """Gets the main windows object of the game."""
        return UserInterface.main_window

    @staticmethod
    def get_app():
        """Gets the game application object."""
        return UserInterface.app


class MainWindow(QMainWindow):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.field_ui = FieldUI(self, self.game)

        self.set_background_color()
        self.set_dimensions()
        self.center_window()
        self.init_status_bar()

        self.setWindowIcon(QIcon('images/small_icon.png'))
        self.setWindowTitle('Falling Rocks')
        self.show()

    def set_background_color(self):
        """Sets the background color of the main window."""
        palette = QPalette()
        palette.setColor(QPalette.Background, Qt.white)
        self.setPalette(palette)

    def center_window(self):
        """Puts the field widget in the center of the main window."""
        self.setCentralWidget(self.field_ui)
        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2,
                  (screen.height() - size.height()) / 2)

    def init_status_bar(self):
        """Initializes the status bar of the game and shows a New game message
        to the user.
        """
        self.communicate = Communicate()
        self.statusbar = self.statusBar()
        self.communicate.message_statusbar[str].\
            connect(self.statusbar.showMessage)
        self.communicate.message_statusbar.emit("New game")

    def set_dimensions(self):
        """Sets the dimensions of the main window."""
        self.height = self.game.dimensions[0]
        self.width = self.game.dimensions[1]
        self.resize(self.height, self.width)

    def restart_game(self):
        """Restarts the game and opens a new game application."""
        self.game.reset_game_values()
        UserInterface.close_app()
        subprocess.call("python" + " falling_rocks.py", shell=True)


class FieldUI(QFrame):
    def __init__(self, parent, game):
        super().__init__(parent)
        self.main_window = parent
        self.game = game
        self.rocks = self.game.rocks
        self.powerups = self.game.powerups
        self.bullets = self.game.bullets
        self.width, self.height = self.game.dimensions

        self.init_timers()
        self.start_timers()

        self.player_ui = PlayerUI(self, self.game)

        self.init_signals()
        self.setFocusPolicy(Qt.StrongFocus)

    def init_timers(self):
        """Initializes the timers in the game."""
        self.game_timer = QBasicTimer()
        self.rock_timer = QBasicTimer()
        self.level_timer = QBasicTimer()
        self.powerup_timer = QBasicTimer()
        self.ticker_timer = QBasicTimer()
        self.bullet_timer = QBasicTimer()

        self.player_invincibility_timer = QBasicTimer()
        self.big_bomb_timer = QBasicTimer()
        self.slow_down_rocks_timer = QBasicTimer()
        self.shoot_rocks_timer = QBasicTimer()

        self.powerup_duration_timer = QTimer()

    def start_timers(self):
        """Starts the timers in the game."""
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        self.level_timer.start(self.game.level_speed, self)
        self.powerup_timer.start(self.game.rock_speed, self)
        self.player_invincibility_timer.start(int(PowerupTimeInterval.medium),
                                              self)
        self.big_bomb_timer.start(int(PowerupTimeInterval.big), self)
        self.slow_down_rocks_timer.start(int(PowerupTimeInterval.medium), self)
        self.shoot_rocks_timer.start(int(PowerupTimeInterval.very_big), self)
        self.bullet_timer.start(self.game.bullet_speed, self)

    def stop_timers(self):
        """Stops the timers in the game."""
        self.game_timer.stop()
        self.rock_timer.stop()
        self.level_timer.stop()
        self.powerup_timer.stop()
        self.ticker_timer.stop()
        self.bullet_timer.stop()

        self.player_invincibility_timer.stop()
        self.big_bomb_timer.stop()
        self.slow_down_rocks_timer.stop()
        self.shoot_rocks_timer.stop()

        self.powerup_duration_timer.stop()

    def init_signals(self):
        """Initializes the signals in the game that connect to a method and
        calls it after the singnals are emitted.
        """
        self.com = Communicate()
        self.com.move_left.connect(self.player_ui.move_left)
        self.com.move_right.connect(self.player_ui.move_right)
        self.com.restart.connect(self.main_window.restart_game)
        self.com.exit.connect(UserInterface.close_app)
        self.com.win.connect(self.win_the_game)

    def timerEvent(self, event):
        """Gets the emitted events from the timers and calls the appropriate
        methods for each of them.
        """
        self.powerups_timer_events(event)
        self.gameplay_timer_events(event)
        if event.timerId() == self.ticker_timer.timerId():
            self.ticker["value"] -= 1
            if self.ticker["type"] == "player_invincibility":
                self.show_player_invincibility_info(self.ticker["value"])
            if self.ticker["type"] == "slow_down_rocks":
                self.show_slow_down_rocks_info(self.ticker["value"])
            if self.ticker["type"] == "shoot_rocks":
                self.show_shoot_rocks_info(self.ticker["value"])
                self.bullet_ui = BulletUI(self, self.game, self.player_ui)
                self.bullets.append(self.bullet_ui)
        else:
            super(FieldUI, self).timerEvent(event)

    def gameplay_timer_events(self, event):
        """Gets the emitted events from the timers related to the gameplay and
        calls the appropriate methods and initializes the appropriate objects
        for each of them.
        """
        if event.timerId() == self.game_timer.timerId():
            self.rock_ui = RockUI(self, self.game)
            self.rocks.append(self.rock_ui)
        elif event.timerId() == self.rock_timer.timerId():
            self.drop_down_rocks()
        elif event.timerId() == self.powerup_timer.timerId():
            self.drop_down_powerups()
        elif event.timerId() == self.level_timer.timerId():
            self.game.level_up()
            self.game_level = self.game.level
            if self.game_level == 21:
                self.com.win.emit()
                return
            self.game.set_speed_after_levelup()
            self.main_window.communicate.message_statusbar.\
                emit("Level " + str(self.game_level))
            self.game_timer.start(self.game.game_speed, self)
            self.rock_timer.start(self.game.rock_speed, self)
        elif event.timerId() == self.bullet_timer.timerId():
            if self.bullets.count != 0:
                self.shoot_bullets()

    def powerups_timer_events(self, event):
        """Gets the emitted events from the timers related to the powerups and
        calls the appropriate methods and initializes the appropriate objects
        for each of them.
        """
        if event.timerId() == self.player_invincibility_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game, PowerupType.
                                        player_invinciblility)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.big_bomb_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game, PowerupType.big_bomb)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.slow_down_rocks_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game,
                                        PowerupType.slow_down_rocks)
            self.powerups.append(self.powerup_ui)
        elif event.timerId() == self.shoot_rocks_timer.timerId():
            self.powerup_timer.start(self.game.rock_speed, self)
            self.powerup_ui = PowerupUI(self, self.game,
                                        PowerupType.shoot_rocks)
            self.powerups.append(self.powerup_ui)

    def win_the_game(self):
        """Wins the game and shows an appropriate message to the player."""
        self.game.win()
        self.stop_timers()
        self.main_window.communicate.message_statusbar.\
            emit("You've won the game. You are a survivor. Well done!")

    def drop_down_powerups(self):
        """Moves the powerups down and check if the move is out of the game
        field. If that is true the powerups are removed from the field.
        """
        temp_powerup = None
        for powerup in self.powerups:
            if(powerup.y >= self.game.dimensions[1] - powerup.height):
                temp_powerup = powerup
            else:
                powerup.drop_down()
            self.check_collision_between_player_and_powerup(powerup)
        if temp_powerup is not None:
            self.remove_powerup_from_field(temp_powerup)

    def check_collision_between_player_and_powerup(self, powerup):
        """Checks for a collision between the player and the powerups. If that
        is true initializes the powerups' effect according to their type.
        """
        if(self.game.collision_detected(self.player_ui, powerup)):
            if powerup.type == PowerupType.player_invinciblility:
                self.init_player_invincibility(powerup)
            elif powerup.type == PowerupType.big_bomb:
                self.init_big_bomb()
            elif powerup.type == PowerupType.slow_down_rocks:
                self.init_slow_down_rocks(powerup)
            elif powerup.type == PowerupType.shoot_rocks:
                self.init_shoot_rocks(powerup)

    def init_slow_down_rocks(self, powerup):
        """Initializes the powerup slow_down_rocks and it's effect of the
        game."""
        self.game.set_rock_speed(self.game.rock_speed + 3)
        self.game.set_speed(self.game.game_speed + 25)
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        self.ticker = {"type": "slow_down_rocks",
                       "value": powerup.duration // 1000}

        self.show_slow_down_rocks_info(self.ticker["value"])
        self.ticker_timer.start(PowerupTimeInterval.second, self)
        self.powerup_duration_timer.setSingleShot(True)
        self.powerup_duration_timer.singleShot(powerup.duration,
                                               self.stop_slow_down_rocks)

    def show_slow_down_rocks_info(self, value):
        """Shows information about the powerup slow_down_rocks to the
        player.
        """
        self.main_window.communicate.message_statusbar.\
            emit("The rock are slowed down for " + str(value) + " seconds")

    def stop_slow_down_rocks(self):
        """Stops the effect of the powerup slow_down_rocks and shows a message
        to the player.
        """
        self.powerup_duration_timer.stop()
        self.ticker_timer.stop()
        self.game.set_rock_speed(self.game.rock_speed - 3)
        self.game.set_speed(self.game.game_speed - 25)
        self.game_timer.start(self.game.game_speed, self)
        self.rock_timer.start(self.game.rock_speed, self)
        self.main_window.communicate.message_statusbar.\
            emit("The rock are no longer slowed down. Be careful!")

    def shoot_bullets(self):
        """Moves the bullets up (to the target) and check if the move is out of
        the game field. If that is true the bullets are removed from the field.
        """
        temp_bullet = None
        for bullet in self.bullets:
            if(bullet.y <= 1):
                temp_bullet = bullet
            else:
                bullet.move_to_target()
                self.check_collision_between_bullet_and_rock(bullet)
        if temp_bullet is not None:
            self.remove_bullet_from_field(temp_bullet)

    def check_collision_between_bullet_and_rock(self, bullet):
        """Checks for a collision between the bullets and the rocks. If that
        is true removes the rocks from the game field.
        """
        for rock in self.rocks:
            if self.game.collision_detected(bullet, rock):
                self.remove_rock_from_field(rock)

    def init_shoot_rocks(self, powerup):
        """Initializes the powerup shoot_rocks and it's effect of the game."""
        self.ticker = {"type": "shoot_rocks",
                       "value": powerup.duration // 1000}
        self.show_shoot_rocks_info(self.ticker["value"])
        self.ticker_timer.start(PowerupTimeInterval.second, self)
        self.powerup_duration_timer.setSingleShot(True)
        self.powerup_duration_timer.singleShot(powerup.duration,
                                               self.stop_shoot_rocks)

    def show_shoot_rocks_info(self, value):
        """Shows information about the powerup shoot_rocks to the player."""
        self.main_window.communicate.message_statusbar.\
            emit("You have bullets for " + str(value) + " seconds")

    def stop_shoot_rocks(self):
        """Stops the effect of the powerup shoot_rocks and shows a message
        to the player.
        """
        self.powerup_duration_timer.stop()
        self.ticker_timer.stop()
        self.main_window.communicate.message_statusbar.\
            emit("No more bullets!")

    def init_big_bomb(self):
        """Initializes the powerup big_bomb and it's effect of the game."""
        temp_rocks = self.rocks[:]
        for temp_rock in temp_rocks:
            self.remove_rock_from_field(temp_rock)
        self.main_window.communicate.message_statusbar.\
            emit("BOOM! The blast totally destroyed everything on the field!")

    def init_player_invincibility(self, powerup):
        """Initializes the powerup player_invincibility and it's effect
        of the game.
        """
        if not self.player_ui.is_player_invincible:
            self.player_ui.set_player_invinciblity()
            self.ticker = {"type": "player_invincibility",
                           "value": powerup.duration // 1000}
            self.show_player_invincibility_info(self.ticker["value"])
            self.ticker_timer.start(PowerupTimeInterval.second, self)
            self.powerup_duration_timer.setSingleShot(True)
            self.powerup_duration_timer.singleShot(
                powerup.duration, self.stop_player_invincibility
            )

    def stop_player_invincibility(self):
        """Stops the effect of the powerup player_invincibility and shows a
        message to the player.
        """
        self.powerup_duration_timer.stop()
        self.ticker_timer.stop()
        self.player_ui.set_player_invinciblity()
        self.main_window.communicate.message_statusbar.\
            emit("The player's invinciblility is off. You are mortal again!")

    def show_player_invincibility_info(self, value):
        """Shows information about the powerup player_invincibility_info to the
        player.
        """
        self.main_window.communicate.message_statusbar.\
            emit("The player is invincible for " + str(value) + " seconds")

    def remove_powerup_from_field(self, powerup):
        """Removes a powerup from the game field."""
        self.powerups.remove(powerup)
        powerup.remove_shape()
        if(self.powerups.count == 0):
            self.powerup_timer.stop()

    def remove_bullet_from_field(self, bullet):
        """Removes a bullet from the game field."""
        self.bullets.remove(bullet)
        bullet.remove_shape()
        if(self.bullets.count == 0):
            self.bullet_timer.stop()

    def remove_rock_from_field(self, rock):
        """Removes a rock from the game field."""
        self.rocks.remove(rock)
        rock.remove_shape()

    def drop_down_rocks(self):
        """Moves the rocks down and check if the move is out of the game
        field. If that is true the rocks are removed from the field.
        """
        temp_rock = None
        for rock in self.rocks:
            if(rock.y >= self.game.dimensions[1] - rock.height - 15):
                temp_rock = rock
            else:
                rock.drop_down()
            self.check_collision_between_rock_and_player(rock)
        if temp_rock is not None:
            self.remove_rock_from_field(temp_rock)

    def check_collision_between_rock_and_player(self, rock):
        """Checks for a collision between the rock and the player. If that is
        true the game is over.
        """
        if(not self.player_ui.is_player_invincible and
           self.game.collision_detected(self.player_ui, rock)):
            self.stop_timers()
            self.game.lose()
            self.main_window.communicate.message_statusbar.\
                emit("Game Over")

    def keyPressEvent(self, event):
        """Gets the events emitted when the player presses a key on the
        keyboard and calls the appropriate method.
        """
        super(FieldUI, self).keyPressEvent(event)
        key = event.key()
        if key == Qt.Key_Escape:
            self.com.exit.emit()
        elif key == Qt.Key_R:
            self.com.restart.emit()
        elif self.game.is_lost:
            return
        elif key == Qt.Key_P:
            if self.game.is_running:
                self.pause_game()
            else:
                self.resume_game()
            return
        if self.game.is_paused:
            return
        elif key == Qt.Key_Left:
            self.com.move_left.emit()
        elif key == Qt.Key_Right:
            self.com.move_right.emit()

    def pause_game(self):
        """Pauses the game and shows a message to the player."""
        if self.game.is_running:
            self.game.pause()
            self.stop_timers()
            self.main_window.communicate.message_statusbar.emit("Paused")

    def resume_game(self):
        """Resumes the game and shows a message to the player."""
        if self.game.is_paused:
            self.game.resume()
            self.start_timers()
            self.main_window.communicate.message_statusbar.emit("Running")
        self.update()
