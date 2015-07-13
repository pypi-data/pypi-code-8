import unittest
from gameplay.rock import Rock
from gameplay.player import Player
from gameplay.bullet import Bullet
from gameplay.field import Field
from gameplay.game import Game
from gui.user_interface import UserInterface
from gui.bullet_ui import BulletUI
from gui.powerup_ui import PowerupUI, PowerupType


class RockTest(unittest.TestCase):
    def setUp(self):
        self.rock = Rock()

    def test_getting_initial_rock_speed(self):
        initial_speed = 50
        self.assertEqual(initial_speed, self.rock.rock_speed)

    def test_setting_new_rock_speed(self):
        new_speed = 60
        self.rock.set_speed(new_speed)
        self.assertEqual(new_speed, self.rock.rock_speed)


class PlayerTest(unittest.TestCase):
    def setUp(self):
        self.player = Player()

    def test_check_initial_player_invinciblity(self):
        self.assertEqual(False, self.player.is_player_invincible)
        self.assertNotEqual(True, self.player.is_player_invincible)

    def test_getting_initial_player_speed(self):
        initial_speed = 10
        self.assertEqual(initial_speed, self.player.player_speed)

    def test_setting_player_invinciblity(self):
        self.player.set_player_invinciblity()
        self.assertEqual(True, self.player.is_player_invincible)
        self.assertNotEqual(False, self.player.is_player_invincible)
        self.player.set_player_invinciblity()
        self.assertEqual(False, self.player.is_player_invincible)
        self.assertNotEqual(True, self.player.is_player_invincible)


class BulletTest(unittest.TestCase):
    def setUp(self):
        self.bullet = Bullet()

    def test_getting_initial_bullet_speed(self):
        initial_speed = 50
        self.assertEqual(initial_speed, self.bullet.bullet_speed)

    def test_setting_new_bullet_speed(self):
        new_speed = 60
        self.bullet.set_speed(new_speed)
        self.assertEqual(new_speed, self.bullet.bullet_speed)


class GameTest(unittest.TestCase):
    def setUp(self):
        self.field = Field(1080, 800)
        self.game = Game(self.field)

    def check_game_field_dimensions(self):
        game_dimensions = (self.field.width, self.field.height)
        self.assertEqual(game_dimensions, self.game.dimensions)

    def test_checking_is_game_lost(self):
        self.assertEqual(False, self.game.is_lost)

    def test_checking_is_game_won(self):
        self.assertEqual(False, self.game.is_won)

    def test_checking_is_game_paused(self):
        self.assertEqual(False, self.game.is_paused)

    def test_checking_is_game_running(self):
        self.assertEqual(True, self.game.is_running)

    def test_checking_is_game_lost_after_losing(self):
        self.game.lose()
        self.assertEqual(True, self.game.is_lost)
        self.assertEqual(False, self.game.is_running)

    def test_checking_is_game_won_after_winning(self):
        self.game.win()
        self.assertEqual(True, self.game.is_won)
        self.assertEqual(False, self.game.is_lost)
        self.assertEqual(False, self.game.is_running)

    def test_checking_is_game_paused_after_pausing(self):
        self.game.pause()
        self.assertEqual(True, self.game.is_paused)
        self.assertEqual(False, self.game.is_running)

    def test_checking_is_game_running_after_resuming(self):
        self.game.resume()
        self.assertEqual(False, self.game.is_paused)
        self.assertEqual(True, self.game.is_running)

    def test_setting_new_game_speed(self):
        new_speed = 300
        self.game.set_speed(new_speed)
        self.assertEqual(new_speed, self.game.game_speed)

    def test_setting_new_rock_speed(self):
        new_speed = 30
        self.game.set_rock_speed(new_speed)
        self.assertEqual(new_speed, self.game.rock_speed)

    def test_leveling_up(self):
        current_level = self.game.level
        self.game.level_up()
        self.assertEqual(current_level + 1, self.game.level)

    def test_getting_initial_game_speed(self):
        initial_speed = 630
        self.assertEqual(initial_speed, self.game.game_speed)

    def test_getting_initial_bullet_speed(self):
        initial_speed = 50
        self.assertEqual(initial_speed, self.game.bullet_speed)

    def test_getting_initial_rock_speed(self):
        initial_speed = 50
        self.assertEqual(initial_speed, self.game.rock_speed)

    def test_getting_initial_level_speed(self):
        initial_speed = 30000
        self.assertEqual(initial_speed, self.game.level_speed)

    def test_getting_initial_level(self):
        initial_level = 1
        self.assertEqual(initial_level, self.game.level)

    def test_get_rock(self):
        rock = self.field.rock
        self.assertEqual(rock, self.game.rock)

    def test_get_bullet(self):
        bullet = self.field.bullet
        self.assertEqual(bullet, self.game.bullet)

    def test_get_powerup(self):
        powerup = self.field.powerup
        self.assertEqual(powerup, self.game.powerup)

    def test_get_player(self):
        player = self.field.player
        self.assertEqual(player, self.game.player)

    def test_get_rocks(self):
        rocks = self.field.rocks
        self.assertEqual(rocks, self.game.rocks)

    def test_get_bullets(self):
        bullets = self.field.bullets
        self.assertEqual(bullets, self.game.bullets)

    def test_get_powerups(self):
        powerups = self.field.powerups
        self.assertEqual(powerups, self.game.powerups)

    def test_resetting_game(self):
        self.game.reset_game_values()
        self.assertEqual(630, self.game.game_speed)
        self.assertEqual(30000, self.game.level_speed)
        self.assertEqual(1, self.game.level)
        self.assertEqual(50, self.game.rock_speed)


class FieldTest(unittest.TestCase):
    def setUp(self):
        self.field = Field(1080, 800)

    def test_getting_initial_bullet_speed(self):
        initial_speed = 50
        self.assertEqual(initial_speed, self.field.bullet.bullet_speed)

    def test_getting_initial_rock_speed(self):
        initial_speed = 50
        self.assertEqual(initial_speed, self.field.rock.rock_speed)

    def test_getting_initial_player_speed(self):
        initial_speed = 10
        self.assertEqual(initial_speed, self.field.player.player_speed)


class GUITest(unittest.TestCase):
    field = Field(1080, 800)
    game = Game(field)
    ui = UserInterface(game)
    ui.main_loop()
    main_window = UserInterface.get_main_window()

    def test_check_main_window_dimensions(self):
        main_window_height = UserInterface.get_main_window().height
        main_window_width = UserInterface.get_main_window().width
        self.assertEqual(1080, main_window_height)
        self.assertEqual(800, main_window_width)

    def test_bullet_moving_to_target(self):
        self.field_ui = GUITest.main_window.field_ui
        self.player_ui = self.field_ui.player_ui
        self.bullet_ui = BulletUI(GUITest.main_window,
                                  GUITest.game, self.player_ui)
        initial_y = self.bullet_ui.y
        self.bullet_ui.move_to_target()
        self.assertGreater(initial_y, self.bullet_ui.y)

    def test_check_pausing_the_game(self):
        self.field_ui = GUITest.main_window.field_ui
        self.field_ui.pause_game()
        self.assertEqual(True, GUITest.game.is_paused)

    def test_check_resuming_the_game(self):
        self.field_ui = GUITest.main_window.field_ui
        self.field_ui.resume_game()
        self.assertEqual(True, GUITest.game.is_running)

    def test_check_leveling_up(self):
        self.game = GUITest.game
        current_level = self.game.level
        self.game.level_up()
        self.assertLess(current_level, self.game.level)

    def test_check_winning_the_game(self):
        GUITest.main_window.field_ui.win_the_game()
        self.assertEqual(True, GUITest.game.is_won)

    def test_check_powerup_dropping_down(self):
        self.field_ui = GUITest.main_window.field_ui
        self.powerup_ui = PowerupUI(GUITest.main_window, GUITest.game,
                                    PowerupType.player_invinciblility)
        initial_y = self.powerup_ui.y
        self.powerup_ui.drop_down()
        self.assertLess(initial_y, self.powerup_ui.y)

if __name__ == '__main__':
    unittest.main()
