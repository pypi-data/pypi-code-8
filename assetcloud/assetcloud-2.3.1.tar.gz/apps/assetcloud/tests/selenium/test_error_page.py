# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from assetcloud.tests.selenium.utils import LoggedInSeleniumTestCase
from django.core.urlresolvers import reverse
from django.test.utils import override_settings


class ServerErrorViewSeleniumTests(LoggedInSeleniumTestCase):
    """
    Note: these tests have to be Selenium, not service tests, because when a
    view raises an exception the Django test client raises that exception
    instead of rendering the error page (see
    https://code.djangoproject.com/ticket/18707).
    """

    @override_settings(PROJECT_NAME='Foo Cloud')
    def test_project_name_in_email_subject(self):
        self.browser.get(self.live_server_url + reverse('raise-exception'))
        link_element = self.find_and_wait(id='id_contact_us')
        self.assertIn('Foo%20Cloud', link_element.attributes['href'])

    @override_settings(SUPPORT_EMAIL_ADDRESS='zzz@xxx.com')
    def test_support_email_address_in_email_subject(self):
        self.browser.get(self.live_server_url + reverse('raise-exception'))
        link_element = self.find_and_wait(id='id_contact_us')
        self.assertIn('zzz@xxx.com', link_element.attributes['href'])
