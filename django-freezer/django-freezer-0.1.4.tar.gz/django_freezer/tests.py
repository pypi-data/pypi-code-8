from django.test import TestCase

from django_freezer.admin import _parse

REQS_WITH_VERSIONS = """Django==1.6
ipdb==0.8
ipython==3.0.0
"""

REQS_WITHOUT_VERSIONS = """Django
ipdb
ipython
"""


class ParseTestCase(TestCase):

    def test_not_a_proper_string(self):
        not_reqs = 'This is just a text, plain text.'
        self.assertEquals(_parse(not_reqs), [[not_reqs]])

    def test_empty_string(self):
        self.assertEquals(_parse(''), [])

    def test_reqs_list_with_versions(self):
        self.assertEquals(_parse(REQS_WITH_VERSIONS),
                          [['Django', '1.6'],
                           ['ipdb', '0.8'],
                           ['ipython', '3.0.0']])

    def test_reqs_list_without_versions(self):
        self.assertEquals(_parse(REQS_WITHOUT_VERSIONS),
                          [['Django'],
                           ['ipdb'],
                           ['ipython']])
