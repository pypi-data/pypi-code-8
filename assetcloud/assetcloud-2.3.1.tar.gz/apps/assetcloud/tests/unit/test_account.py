# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from .utils import UnitTestCase
from assetcloud_auth.forms import AccountForm


class AccountFormTests(UnitTestCase):
    def test_account_form_creates_account(self):
        name = 'test'
        form = AccountForm({'name': name})
        self.assertTrue(form.is_valid())
        account = form.save()
        self.assertEqual(account.name, name)

    def test_account_form_does_not_have_fields_it_shouldnt(self):
        form = AccountForm()
        for field_name in (
            'welcome_text',
            'logo',
            'header_background',
            'header_links',
            'header_links_active',
        ):
            with self.assertRaises(KeyError):
                #noinspection PyStatementEffect
                form.fields[field_name]
