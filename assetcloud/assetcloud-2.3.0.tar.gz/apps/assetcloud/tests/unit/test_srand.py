# -*- coding: utf-8 -*-
# (c) 2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud import srand
import django.utils.unittest


class SRandUnicodeTests(django.utils.unittest.TestCase):
    tags = ['unit', ]

    # Note: these tests are very basic and they don't test that the RNG is
    # cryptographically secure (e.g. that it is not predictable).

    def test_chars_are_in_required_range(self):
        ru = srand.random_alphanumeric(1000)
        alpha_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

        self.assertEqual(1000, len(ru))
        for c in ru:
            self.assertIn(c, alpha_chars)

    def test_chars_arent_all_same(self):
        ru = srand.random_alphanumeric(10)
        self.assertEqual(10, len(ru))

        all_same = True
        first = ru[0]
        for c in ru[1:]:
            if c != first:
                all_same = False
                break

        self.assertFalse(all_same)
