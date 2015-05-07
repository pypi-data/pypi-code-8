# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.tests.service.utils import TestCase
from django.core.urlresolvers import reverse
from raiseexception import DeliberateException


class SystemTests(TestCase):
    """Tests for the system administration views"""

    def test_raise_exception_view_raises_exception(self):
        self.client.login()
        self.assertRaises(
            DeliberateException,
            self._call_raise_exception_view)

    def _call_raise_exception_view(self):
        self.client.get(reverse('raise-exception'))
