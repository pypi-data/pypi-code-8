# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.tests.service.utils import LoggedInTestCase, create_viewer, create_asset
from django.core.urlresolvers import reverse
from django.conf import settings


class AssetsPageTests(LoggedInTestCase):
    def test_asset_page_has_google_analytics_set(self):
        settings.GOOGLE_ANALYTICS_KEY = 'test_key'
        response = self.client.get(reverse('asset-list'))
        self.assertContains(response, 'test_key')

    def test_asset_list_page_has_search_filter(self):
        """
        Ensure that the search filter panel is shown on the home page
        """
        response = self.client.get(reverse('asset-list'))
        self.assertContains(response, '<h4 class="no-top-margin">Filters</h4>')

    def test_asset_page_has_get_started_if_no_assets(self):
        response = self.client.get(reverse('asset-list'))
        self.assertContains(response, 'Get Started')

    def test_asset_page_has_no_get_started_if_assets(self):
        create_asset(account=self.account)
        response = self.client.get(reverse('asset-list'))
        self.assertNotIn('Get Started', response.content)

    def test_asset_page_has_no_get_started_if_cannot_edit(self):
        user = create_viewer()
        self.client.login(user)
        response = self.client.get(reverse('asset-list'))
        self.assertNotIn('Get Started', response.content)

default_welcome_text = 'Welcome to Asset Share, ' \
                       'a tool for sharing and managing your digital assets.'


class WelcomeTextTests(LoggedInTestCase):
    def assertWelcomeTextIn(self, url=None, welcome_text=None):
        response = self.client.get(reverse(url), follow=True)
        self.assertIn(welcome_text, response.content)

    def assertWelcomeTextNotIn(self, url=None, welcome_text=None):
        response = self.client.get(reverse(url), follow=True)
        self.assertNotIn(welcome_text, response.content)

    def test_homepage_shows_welcome_text(self):
        self.account.welcome_text = 'Test welcome text'
        self.account.save()
        self.assertWelcomeTextIn(url='home',
                                 welcome_text=self.account.welcome_text)

    def test_homepage_shows_default_text_if_no_welcome_text(self):
        self.assertWelcomeTextIn(url='home',
                                 welcome_text=default_welcome_text)

    def test_asset_page_does_not_show_welcome_text_if_not_set(self):
        self.assertWelcomeTextNotIn(url='asset-list',
                                    welcome_text=default_welcome_text)

    def test_asset_page_does_not_show_welcome_text_if_set(self):
        self.account.welcome_text = 'Test welcome text'
        self.account.save()
        self.assertWelcomeTextNotIn(url='asset-list',
                                    welcome_text=self.account.welcome_text)
