from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from nose.tools import eq_

from standbydb import (DEFAULT_DB_ALIAS, MasterStandbyRouter, get_standby)


class MasterSlaveRouterTests(TestCase):
    """Tests for MasterSlaveRouter"""

    def test_db_for_read(self):
        eq_(MasterStandbyRouter().db_for_read(None), get_standby())
        # TODO: Test the round-robin functionality.

    def test_db_for_write(self):
        eq_(MasterStandbyRouter().db_for_write(None), DEFAULT_DB_ALIAS)

    def test_allow_syncdb(self):
        """Make sure allow_syncdb() does the right thing for both masters and
        slaves"""
        router = MasterStandbyRouter()
        assert router.allow_syncdb(DEFAULT_DB_ALIAS, None)
        assert not router.allow_syncdb(get_standby(), None)









