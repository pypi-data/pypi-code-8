# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.tests.service.utils import TestCase


class DateFormatTests(TestCase):
    def assertLocaleEquals(self, accepted=None, locale=None):
        d = {'HTTP_ACCEPT_LANGUAGE': accepted}
        response = self.client.get('home', follow=True, **d)
        self.assertIn('LOCALE = "%s"' % locale, response.content)

    def test_locale_set_for_en(self):
        self.assertLocaleEquals(accepted="en", locale="en")
        self.assertLocaleEquals(accepted="EN", locale="en")

    def test_locale_set_for_en_us(self):
        self.assertLocaleEquals(accepted="en-us", locale="en")
        self.assertLocaleEquals(accepted="EN-US", locale="en")

    def test_locale_set_for_en_gb(self):
        self.assertLocaleEquals(accepted="en-gb", locale="en_GB")
        self.assertLocaleEquals(accepted="EN-GB", locale="en_GB")

    def test_locale_set_for_invalid(self):
        self.assertLocaleEquals(accepted="invalid", locale="en_GB")
