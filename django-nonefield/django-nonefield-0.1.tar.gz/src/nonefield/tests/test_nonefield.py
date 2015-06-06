__all__ = ('NoneFieldTest',)
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = 'Copyright (c) 2015 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'

import unittest

from django import forms
from django.test import RequestFactory, TestCase
from nonefield.fields import NoneField
from nonefield.tests.base import print_info
from nonefield.tests.constants import (
    ENDPOINT_URL, INITIAL_NONEFIELD_VALUE, CHANGED_NONEFIELD_VALUE
    )

class MyForm(forms.Form):
    """
    Test form.
    """
    name = forms.CharField(required=True)
    static_text = NoneField(initial=INITIAL_NONEFIELD_VALUE)

class NoneFieldTest(TestCase):
    """
    Test the django-nonefield package.
    """
    def setUp(self):
        """
        :return:
        """

    @print_info
    def test_01_nonefield(self):
        """
        Test `nonefield.fields.NoneField`.
        """
        request_factory = RequestFactory()
        request = request_factory.post(
            ENDPOINT_URL,
            data={'name': "John Doe", 'static_text': CHANGED_NONEFIELD_VALUE}
            )

        form = MyForm(
            data=request.POST,
            initial={'static_text': INITIAL_NONEFIELD_VALUE}
            )

        self.assertTrue("John Doe" == form.cleaned_data['name'])
        self.assertTrue(INITIAL_NONEFIELD_VALUE == form.cleaned_data['static_text'])
        return res


if __name__ == '__main__':
    unittest.main()
