# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from django.core.urlresolvers import reverse

from .utils import TestCase


class NavigationTests(TestCase):
    """
    Service tests for the site navigation
    """

    def test_home_page_has_asset_list_link(self):
        self.client.login()
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'assets', status_code=200)
