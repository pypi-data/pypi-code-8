# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from .utils import SeleniumTestCase
from selenium.common.exceptions import NoSuchElementException


class LoginSeleniumTests(SeleniumTestCase):
    temp_media_root = False

    def test_login(self):
        # Make sure we're on the login page
        self.assertIsNotNone(self.find_and_wait(id='login-submit'))

        # Login using superclass method
        self.login()

        # Make sure we're not on the login page any more
        with self.assertRaises(NoSuchElementException):
            self.browser.find_element_by_id('login-submit')
        # ...and look for the welcome text, to verify that we're on the home page
        self.browser.find_element_by_id("welcome-text")
