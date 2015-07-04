# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime
from dateutil.relativedelta import relativedelta
from model_mommy import mommy

from django.test import TestCase

from ..models import Sponsor


class SponsorModel(TestCase):
    """
    TestCase for model Sponsor
    """

    def setUp(self):
        super(SponsorModel, self).setUp()
        mommy.make('Sponsor', _quantity=1)

    def test_get_all_sponsors(self):
        """
        Test get_all_sponsors() classmethod returns when exists objects
        """
        self.assertEqual(Sponsor.get_all_sponsors().count(), 1)

    def test_get_expired_sponsors(self):
        """
        Test get_expired_sponsors() classmethod
        """
        mommy.make('Sponsor', does_expire=True, expires_on=datetime.datetime.now()+relativedelta(months=-1))
        self.assertEqual(Sponsor.get_expired_sponsors().count(), 1)

    def test_get_disabled_sponsors(self):
        """
        Test get_disabled_sponsors() classmethod
        """
        mommy.make('Sponsor', enabled=False, _quantity=3)
        self.assertEqual(Sponsor.get_disabled_sponsors().count(), 3)

