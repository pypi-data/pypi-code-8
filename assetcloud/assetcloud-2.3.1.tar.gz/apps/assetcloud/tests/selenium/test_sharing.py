# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud.models import Share
from assetcloud.tests.selenium.utils import LoggedInSeleniumTestCase
from assetcloud.tests.service.utils import create_asset
from django.core.urlresolvers import reverse


class SharingSeleniumTests(LoggedInSeleniumTestCase):
    def test_share_single_from_asset_detail_page(self):
        asset = create_asset(account=self.account)

        self.browser.get(self.live_server_url + reverse('asset', kwargs={'id': asset.id}))
        expected_asset_ids = {asset.id}

        self.assertFalse(Share.objects.exists())

        self.find_and_wait(id="id_share").click()

        self.wait_for_display(id="id_recipient")
        self.browser.find(id="id_recipient").send_keys("nobody@bright-interactive.co.uk")
        self.browser.find(id="share-submit").click()
        self.find_and_wait(css='.alert-success')

        share = Share.objects.get()
        shared_asset_ids = {shared_asset.asset_id for shared_asset
                            in share.shared_assets.all()}
        self.assertEqual(expected_asset_ids, shared_asset_ids)

    def test_share_multiple(self):
        assets = [create_asset(account=self.account) for i in range(3)]
        expected_asset_ids = {asset.id for asset in assets}

        self.find_and_wait(id="id_nav_asset_list").click()
        self.find_and_wait(id="select-all").click()
        self.find_and_wait(id="bulk-share-action").click()

        self.assertFalse(Share.objects.exists())

        self.wait_for_display(id="id_recipient")
        self.browser.find(id="id_recipient").send_keys("nobody@bright-interactive.co.uk")
        self.browser.find(id="share-submit").click()
        self.find_and_wait(css='.alert-success')

        share = Share.objects.get()
        shared_asset_ids = {shared_asset.asset_id for shared_asset
                            in share.shared_assets.all()}
        self.assertEqual(expected_asset_ids, shared_asset_ids)
