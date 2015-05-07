# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from .utils import LoggedInSeleniumTestCase
from assetcloud.tests.service.utils import create_asset
from assetcloud.models import Asset


class ActionsSeleniumTests(LoggedInSeleniumTestCase):
    def test_bulk_delete(self):
        for i in range(3):
            create_asset(account=self.account)

        self.find_and_wait(id="id_nav_asset_list").click()
        self.find_and_wait(id="select-all").click()
        self.find_and_wait(link_text="Delete").click()
        self.wait_for_display(css=".btn-danger")
        self.assertTrue(Asset.unrestricted_objects.exists())
        self.find_and_wait(class_name="btn-danger").click()
        self.find_and_wait(css='.alert-success')
        self.assertFalse(Asset.unrestricted_objects.exists())
