# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from .utils import UnitTestCase
from assetcloud.forms import SearchForm


class SearchFormTests(UnitTestCase):

    def test_empty_form_is_bound(self):
        form = SearchForm({}, user=None)
        self.assertTrue(form.is_bound)

    def test_empty_form_is_valid(self):
        form = SearchForm({}, user=None)
        self.assertTrue(form.is_valid())

    def test_unbound_form_is_not_valid(self):
        form = SearchForm(None, user=None)
        self.assertFalse(form.is_valid())
