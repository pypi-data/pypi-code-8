# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from bs4 import BeautifulSoup
from assetcloud.tests.service.utils import  LoggedInTestCase
from django.core.urlresolvers import reverse
import logging


logger = logging.getLogger(__name__)


class AssetNavTests(LoggedInTestCase):

    def setUp(self):
        super(AssetNavTests, self).setUp()
        self.asset = self.create_asset()
        self.asset_url = reverse('asset', kwargs={'id': self.asset.id})

    def test_no_asset_list_page_initially(self):
        self.assertIsNone(self.get_back_link_soup())

    def test_visiting_asset_list_pages_without_params_sets_list_page(self):
        for asset_list_url in [
            reverse('home'),
            reverse('asset-list'),
            reverse('favourites'),
        ]:
            logger.debug('checking asset list url %s', asset_list_url)
            self.client.get(asset_list_url)
            self.assertEqual(asset_list_url, self.get_back_link_soup()['href'])

    def test_visiting_search_sets_list_page_including_params(self):
        search_url = reverse('search')
        self.client.get(search_url, data={'q': 'looking for this'})
        self.assertEqual(search_url + '?q=looking+for+this',
                         self.get_back_link_soup()['href'])

    def get_back_link_soup(self):
        response = self.client.get(self.asset_url)
        self.assertEqual(response.status_code, 200)
        response_soup = BeautifulSoup(response.content)
        return response_soup.find(id='asset-back-link')
