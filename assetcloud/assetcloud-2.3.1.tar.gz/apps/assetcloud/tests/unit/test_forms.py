# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.core.exceptions import ValidationError
from assetcloud_auth.forms import UpdateUserForm
from assetcloud.fields import ClientsideTagField
from .utils import UnitTestCase


class UpdateUserFormTests(UnitTestCase):
    def test_clean_role_valid(self):
        for role in ['admin', 'editor', 'viewer']:
            form = UpdateUserForm()
            form.cleaned_data = {'role': role}
            # role is valid, so this shouldn't raise a ValidationError
            form.clean_role()

    def test_clean_role_invalid(self):
        form = UpdateUserForm()
        form.cleaned_data = {'role': 'notvalid'}
        with self.assertRaises(ValidationError):
            form.clean_role()


class ClientsideTagFieldTests(UnitTestCase):
    def test_tags_valid(self):
        field = ClientsideTagField()
        self.assertEqual(['valid', 'json'],
                         field.clean('["valid", "json"]'))

    def test_tags_invalid(self):
        field = ClientsideTagField()
        with self.assertRaises(ValidationError):
            field.clean('invalid", "json"]')
