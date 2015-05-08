# -*- coding: utf-8 -*-
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.templatetags.taggit_utils import tag_escape
from .utils import UnitTestCase


class TagEscapeTests(UnitTestCase):
    def test_simple_string_passed_through(self):
        self.assertEqual(
            "simple",
            tag_escape("simple"))

    def test_comma_escaped(self):
        self.assertEqual(
            '"with,comma"',
            tag_escape('with,comma'))

    def test_space_escaped(self):
        self.assertEqual(
            '"with space"',
            tag_escape('with space'))
