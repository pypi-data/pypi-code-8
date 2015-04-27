import unittest


class Game(object):
    def __init__(self):
        self.score = None

    @property
    def played(self):
        return bool(self.score)

    def __unicode__(self):
        if self.score is None:
            return self.player
        else:
            return '%s (score: %s)' % (self.player, self.score)


class InitializationTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()

    def test_default_played_status_is_false(self):
        self.assertEqual(self.game.played, False)

    def test_connects_to_server(self):
        import time
        time.sleep(0.01)


class UpdateTest(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.player = 'Jean-Louis'
        self.game.score = 4

    def test_played_status_is_true_if_score_is_set(self):
        self.assertEqual(self.game.played, True)

    def test_string_representation_is_player_with_score_if_played(self):
        self.assertEqual(unicode(self.game), 'Jean-Louis (score: 4)')

    def test_string_representation_is_only_player_if_not_played(self):
        # See bug #2780
        self.game.score = None
        self.assertEqual(unicode(self.game), 'Jean-Louis')
