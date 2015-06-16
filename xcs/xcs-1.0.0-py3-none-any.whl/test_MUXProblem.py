__author__ = 'Aaron Hosford'

import unittest

from xcs.problems import MUXProblem

class TestMUXProblem(unittest.TestCase):

    def setUp(self):
        self.problem = MUXProblem(10)

    def test_get_possible_actions(self):
        actions = self.problem.get_possible_actions()
        self.assertTrue(len(actions) == 2)
        self.assertTrue(True in actions)
        self.assertTrue(False in actions)

    def test_sense(self):
        previous = self.problem.sense()
        address = previous
        while self.problem.more():

        self.fail()

    def test_execute(self):
        self.fail()

    def test_more(self):
        self.fail()
