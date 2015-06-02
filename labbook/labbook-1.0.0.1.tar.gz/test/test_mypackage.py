import unittest

import labbook


class GeneralTests(unittest.TestCase):
    def test_basics(self):
        self.assertEqual('result', labbook.a_function_of_mine())
        
        m = labbook.MyClass()
        self.assertEqual('another result', m.a_method_of_mine())
