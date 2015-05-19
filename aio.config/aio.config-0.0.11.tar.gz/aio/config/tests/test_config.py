import os
import unittest

from aio.testing import aiotest
import aio.config
import aio.testing
from aio.config.tests import (
    example_module, example_module2)

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
    def test_parse_config_modules(self):
        """
        this test should parse config from multiple paths
        """
        config = yield from aio.config.parse_config(
            modules=[
                aio.testing, aio.config,
                example_module, example_module2])

        # check interpolation between the module conf
        self.assertEqual(
            "default",
            config['more_settings']['example_option2'])
        self.assertEqual(
            "default",
            config['even_more_settings']['example_option'])        
        
    @aiotest
    def test_parse_config_app_dir(self):
        """
        this test should find and parse "aio.conf" in the app_dir
        """
        app_dir = os.path.join(
            TEST_DIR, "resources")
        config = yield from aio.config.parse_config(app_dir=app_dir)
        self.assertEqual(config.sections(), ["section1"])
        self.assertEqual(config["section1"]["result"], "1")

    @aiotest
    def test_parse_custom_config(self):
        """
        this test should parse a custom config file
        """
        configfile = os.path.join(
            TEST_DIR, "resources", "test-1.conf")
        config = yield from aio.config.parse_config(configfile)
        self.assertEqual(config.sections(), ["foo", "bar"])
        self.assertEqual(config["foo"]["bar"], "1")
        self.assertEqual(config["bar"]["foo"], "baz")

    @aiotest
    def test_config_string(self):
        config = yield from aio.config.parse_config(
            config_string=CONFIG_STRING)
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
            aio.config.find_config(app_dir),
            os.path.join(
                app_dir, 'aio.conf'))

    def test_find_config_etc(self):
        """
        this test should find "aio.conf" in the etc
        """
        app_dir = os.path.join(
            TEST_DIR, "resources", "sub")
        self.assertEqual(
            aio.config.find_config(app_dir),
            os.path.join(
                app_dir, "etc", 'aio.conf'))



class AioConfigGatherTestCase(unittest.TestCase):

    def test_gather_config(self):

        from aio.config.tests import (
            example_module, example_module2)
        
        config_files = aio.config.gather_config(
            [aio.testing, aio.config,
             example_module, example_module2])

        expected = [
            os.path.join(m.__path__[0], "aio.conf")
            for m in [example_module, example_module2]]

        self.assertEqual(config_files, expected)

    def test_gather_config_custom_filename(self):
        
        config_files = aio.config.gather_config(
            [aio.testing, aio.config,
             example_module, example_module2])

        expected = [
            os.path.join(m.__path__[0], "aio.conf")
            for m in [example_module, example_module2]]

        self.assertEqual(config_files, expected)
