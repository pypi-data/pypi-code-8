# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from selenium.webdriver.common.keys import Keys
from .utils import LoggedInSeleniumTestCase
from assetcloud.tests.service.utils import create_asset
import datetime


class SearchFilterSeleniumTests(LoggedInSeleniumTestCase):
    def setUp(self):
        super(SearchFilterSeleniumTests, self).setUp()
        create_asset(account=self.account)
        self.find_and_wait(id="id_nav_asset_list").click()

    def format_date(self, date):
        return date.strftime('01/01/%Y')

    def get_from_date_input(self):
        self.wait_for_display(id="id_from_date")
        return self.find_and_wait(id="id_from_date")

    def get_until_date_input(self):
        self.wait_for_display(id="id_until_date")
        return self.find_and_wait(id="id_until_date")

    def set_date_in_field(self, field, date):
        field.send_keys(self.format_date(date) + Keys.TAB)

    def apply_date_filter(self):
        date = datetime.datetime.now()
        from_date = date + datetime.timedelta(days=-400)
        until_date = date + datetime.timedelta(days=400)

        self.find_and_wait(link_text="Specify date range…").click()
        self.set_date_in_field(self.get_from_date_input(), from_date)
        self.set_date_in_field(self.get_until_date_input(), until_date)
        self.find_and_wait(id="apply_date_filters").click()

    def click_last_upload(self):
        self.find_and_wait(id='last_upload_link').click()

    def test_last_upload_visible_after_specifying_date_filter(self):
        self.apply_date_filter()
        self.assertTrue(self.find_and_wait(id='last_upload_link').is_displayed)

    def test_date_filter_visible_after_specifying_date_filter(self):
        self.click_last_upload()
        self.assertTrue(
            self.find_and_wait(link_text="Specify date range…").is_displayed)

    def test_last_upload_takes_priority_over_pre_existing_date_filter(self):
        self.apply_date_filter()
        self.click_last_upload()
        self.assertTrue(
            self.find_and_wait(link_text="Specify date range…").is_displayed)

    def test_date_filter_takes_priority_over_pre_existing_last_upload(self):
        self.click_last_upload()
        self.apply_date_filter()
        self.find_and_wait(text="Specify date range:")
        self.assertTrue(self.find_and_wait(id='last_upload_link').is_displayed)
