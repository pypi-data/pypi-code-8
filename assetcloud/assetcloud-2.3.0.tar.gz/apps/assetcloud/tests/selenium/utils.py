# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.tests.service.utils import MediaRootMover
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from selenium.webdriver.support.ui import WebDriverWait
import test_extras.webdriverplus

# username/password for the superuser created by fixtures

SUPERUSER_USERNAME = 'selenium@bright-interactive.co.uk'
SUPERUSER_PASSWORD = 'xu0EleW9'

# Timeout for long operations, e.g. file uploads. Longer than
# WebDriverPlusTestCase.PAGE_TIMEOUT_SECONDS.
LONG_PAGE_TIMEOUT_SECONDS = 30


class SeleniumTestCase(test_extras.webdriverplus.WebDriverPlusTestCase):
    tags = ['selenium', ]
    temp_media_root = True

    def setUp(self):
        super(SeleniumTestCase, self).setUp()

        if self.temp_media_root:
            self.media_root_mover = MediaRootMover()
            self.media_root_mover.setup_temp_media_root()

        # Start the browser on the front page
        self.browser.get(self.live_server_url + reverse("home"))
        self.browser.maximize_window()

    def tearDown(self):
        super(SeleniumTestCase, self).tearDown()

        if self.temp_media_root:
            self.media_root_mover.teardown_temp_media_root()

    def login(self):
        """
        Login as whatever user we usually want to use for most of the
        tests. This is a superuser for now, but we might change that later.
        """
        sel = self.browser

        self._wait_for_login_or_logout_elements()

        # Log out if already logged in
        logout_element = sel.find(id='logout')
        if logout_element:
            logout_element.click()

        # Fill in login form and submit it
        self.find_and_wait(name='username').send_keys(SUPERUSER_USERNAME)
        self.browser.find(name='password').send_keys(SUPERUSER_PASSWORD)
        self.user = User.objects.get(email=SUPERUSER_USERNAME)
        self.account = self.user.get_profile().account
        self.browser.find(id='login-submit').click()

        # Wait for next page and make sure it has logout element on it to check
        # that login succeeded
        self.find_and_wait(id='logout')

    def _wait_for_login_or_logout_elements(self):
        """
        Wait for EITHER the login form or the logout link in the nav to load
        """
        WebDriverWait(self.browser, self.PAGE_TIMEOUT_SECONDS).until(
            lambda browser: browser.find(id='logout') or browser.find(id='login-submit')
        )

    def wait_for_display(self, timeout=test_extras.webdriverplus.WebDriverPlusTestCase.PAGE_TIMEOUT_SECONDS,
                         **kwargs):
        def wait(browser):
            el = browser.find(**kwargs)
            if el:
                return el.is_displayed
            return False
        return WebDriverWait(self.browser, timeout).until(wait)

    def reverse(self, name):
        """
        Perform a reverse(), and return the absolute url for that
        address on the live server.
        """
        return self.live_server_url + reverse(name)

    def show_no_script(self):
        """
        Show no-script (JavaScript turned off) elements
        """
        self.find_and_wait(css='.no-script').style.display = 'block'

    def selenium_user(self):
        return User.objects.get(email=SUPERUSER_USERNAME)

    def selenium_user_account(self):
        account = self.selenium_user().get_profile().account
        return account


class LoggedInSeleniumTestCase(SeleniumTestCase):
    def setUp(self):
        super(LoggedInSeleniumTestCase, self).setUp()
        self.login()
