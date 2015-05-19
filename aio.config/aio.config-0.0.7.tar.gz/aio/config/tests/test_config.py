import os
import unittest

from aio.testing import aiotest
from aio.config import parse_config, find_config

TEST_DIR = os.path.dirname(__file__)

CONFIG_STRING = """
[section1]
bar: 1
foo: 2

[section2]
bar: 3
foo: 4
"""


class AioConfigParseTestCase(unittest.TestCase):

    @aiotest
    def test_parse_config(self):
        """
        this test should find and parse "aio.conf" in the app_dir
        """
        app_dir = os.path.join(
            TEST_DIR, "resources")
        config = yield from parse_config(app_dir=app_dir)
        self.assertEqual(config.sections(), ["section1"])
        self.assertEqual(config["section1"]["result"], "1")

    @aiotest
    def test_parse_custom_config(self):
        """
        this test should parse a custom config file
        """
        configfile = os.path.join(
            TEST_DIR, "resources", "test-1.conf")
        config = yield from parse_config(configfile)
        self.assertEqual(config.sections(), ["foo", "bar"])
        self.assertEqual(config["foo"]["bar"], "1")
        self.assertEqual(config["bar"]["foo"], "baz")

    @aiotest
    def test_config_string(self):
        config = yield from parse_config(config_string=CONFIG_STRING)
        self.assertEqual(config.sections(), ["section1", "section2"])
        self.assertEqual(config["section1"]["foo"], "2")
        self.assertEqual(config["section2"]["bar"], "3")


class AioConfigFinderTestCase(unittest.TestCase):

    def test_find_config(self):
        """
        this test should find "aio.conf" in the app_dir
        """
        app_dir = os.path.join(
            TEST_DIR, "resources")
        self.assertEqual(
            find_config(app_dir),
            os.path.join(
                app_dir, 'aio.conf'))

    def test_find_config_etc(self):
        """
        this test should find "aio.conf" in the etc
        """
        app_dir = os.path.join(
            TEST_DIR, "resources", "sub")
        self.assertEqual(
            find_config(app_dir),
            os.path.join(
                app_dir, "etc", 'aio.conf'))
