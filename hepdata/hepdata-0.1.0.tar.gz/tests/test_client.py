#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_client
----------------------------------

Tests for `hepdata.client` module.
"""

import unittest

from hepdata import client
from hepdata import exceptions


class TestClient(unittest.TestCase):

    def test_url(self):
        c = client.GiftsClient("AABBCC")

        self.assertEqual(
            c._get_url("profiles"),
            "http://automatch.matchinggifts.com/profiles/xml/AABBCC/",
        )

        self.assertEqual(
            c._get_url("profiles", 1234),
            "http://automatch.matchinggifts.com/profiles/xml/AABBCC/1234/",
        )

        self.assertEqual(
            c._get_url("profiles", 1234, city="Arlington, VA"),
            "http://automatch.matchinggifts.com/profiles/xml/AABBCC/1234/?city=Arlington%2C+VA",
        )


if __name__ == '__main__':
    unittest.main()
