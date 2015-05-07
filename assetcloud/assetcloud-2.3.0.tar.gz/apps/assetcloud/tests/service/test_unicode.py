# -*- coding: utf-8 -*-
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from .utils import TestCase
from django.conf import settings


class UnicodeTests(TestCase):
    def test_wide_unicode_characters_supported(self):
        if settings.WIDE_CHAR_TESTS:
            # This will throw an exception if Python has been built without
            # support for Unicode code points > 0xffff. To fix, rebuild
            # Python and at the configure stage pass --enable-unicode=ucs4.
            unichr(0x10ffff)
