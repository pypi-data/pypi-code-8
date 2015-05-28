#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_netuitive
----------------------------------

Tests for `netuitive` module.
"""

import unittest

import netuitive


class TestClientInit(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        a = netuitive.Client('a', 'b')
        self.failUnlessEqual(a.url, 'a')
        self.failUnlessEqual(a.api_key, 'b')

    def tearDown(self):
        pass


class TestElementInit(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        a = netuitive.Element()
        self.failUnlessEqual(a.type, 'Server')

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
