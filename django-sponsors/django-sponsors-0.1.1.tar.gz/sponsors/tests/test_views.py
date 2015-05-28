# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from model_mommy import mommy

from django.core.urlresolvers import reverse
from django.test import TestCase, Client


class SponsorsView(TestCase):
    """
    TestCase for view ...
    """

    def setUp(self):
        super(SponsorsView, self).setUp()

    def test_list_ok(self):
        """
        GET /sponsors
        """
        url = reverse('list-sponsors')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)

