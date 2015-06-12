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
        b = netuitive.Element('NOT_SERVER')

        self.failUnlessEqual(a.type, 'SERVER')
        self.failUnlessEqual(b.type, 'NOT_SERVER')

    def tearDown(self):
        pass


class TestElementAttributes(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        a = netuitive.Element()
        a.add_attribute('Test', 'TestValue')
        self.failUnlessEqual(a.attributes[0].name, 'Test')
        self.failUnlessEqual(a.attributes[0].value, 'TestValue')

    def tearDown(self):
        pass


class TestElementTags(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        a = netuitive.Element()
        a.add_tag('Test', 'TestValue')

        self.failUnlessEqual(a.tags[0].name, 'Test')
        self.failUnlessEqual(a.tags[0].value, 'TestValue')

    def tearDown(self):
        pass


class TestElementSamples(unittest.TestCase):

    def setUp(self):
        pass

    def test(self):
        a = netuitive.Element()
        a.add_sample(
            'metricId', 1434110794, 1, 'COUNTER', host='hostname')

        self.failUnlessEqual(a.id, 'hostname')
        self.failUnlessEqual(a.name, 'hostname')

        self.failUnlessEqual(a.metrics[0].id, 'metricId')
        self.failUnlessEqual(a.metrics[0].type, 'COUNTER')

        self.failUnlessEqual(a.samples[0].metricId, 'metricId')
        self.failUnlessEqual(a.samples[0].timestamp, 1434110794000)
        self.failUnlessEqual(a.samples[0].val, 1)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
