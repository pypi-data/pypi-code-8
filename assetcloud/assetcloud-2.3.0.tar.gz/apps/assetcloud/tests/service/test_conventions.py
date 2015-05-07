# -*- coding: utf-8 -*-
# (c) 2012 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

"""
Tests that enforce coding conventions
"""

from assetcloud.tests.service.utils import TestCase
from django.db.models.loading import get_app, get_models
from django.utils import unittest as ut2
from modulefinder import ModuleFinder
from assetcloud.models import NullableCharField
import assetcloud.tests.unit
import os


APPS_TO_TEST = [
    'assetcloud',
    'assetcloud_auth',
    ]


class ConventionsTests(TestCase):
    def test_string_fields_not_nullable(self):
        """
        String fields should not have null=True according to
        https://docs.djangoproject.com/en/1.4/ref/models/fields/#django.db.models.Field.null
        """
        for app_name in APPS_TO_TEST:
            app = get_app(app_name)
            for model in get_models(app):
                self._assert_string_fields_not_nullable(model)

    def _assert_string_fields_not_nullable(self, model):
        for field in model._meta.fields:
            self._assert_not_nullable_if_string_field(field)

    def _assert_not_nullable_if_string_field(self, field):
        if self._is_string_field(field):
            self.assertFalse(field.null, '%s.%s.%s is a %s and has null=True' %
                                         (field.model.__module__,
                                          field.model.__name__,
                                          field.name,
                                          field.__class__))

    def _is_string_field(self, field):
        return field.get_internal_type() in {'CharField', 'TextField'} and field.__class__ != NullableCharField


class DependencyTests(ut2.TestCase):
    tags = ['service', 'slow']

    def test_unit_tests_arent_really_service_tests(self):
        """
        If a unit test module imports anything from the service test module
        then that's a sign that the unit test module contains some things
        that are really unit tests, not service tests.
        """
        basedir = os.path.dirname(assetcloud.tests.unit.__file__)
        for dirpath, dirnames, filenames in os.walk(basedir):
            pyfilenames = [filename for filename in filenames
                           if filename.endswith('.py')]
            for pyfilename in pyfilenames:
                pyfilepath = os.path.join(dirpath, pyfilename)
                self.assertFileDoesNotImportServiceTests(pyfilepath)

    def assertFileDoesNotImportServiceTests(self, pyfilepath):
        finder = ModuleFinder()
        finder.run_script(pyfilepath)
        for (module_name, module) in finder.modules.iteritems():
            if module_name == 'assetcloud.tests.service' or \
               module_name.startswith('assetcloud.tests.service.'):
                self.fail('Unit tests should not import anything from assetcloud.tests.service. %s imports %s' % (pyfilepath, module_name))
