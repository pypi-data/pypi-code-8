from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase

from mirrors.models import Component


# class AutocompleteTest(TestCase):
#     def setUp(self):
#         # Create a bunch of components that have the same author and the same
#         # schema
#         for i in range(5):
#             c = Component.objects.create(
#                 slug='test-component-'+str(i),
#                 year=2014,
#                 month=12,
#                 content_type='none',
#                 schema_name='test_schema'
#             )
#             c.new_revision(metadata={
#                 'title': 'test component '+str(i),
#                 'author': 'Bob Avakian'
#             })

#         # Make a component with some different stuff
#         c = Component.objects.create(
#             slug='test-article-component',
#             year=2014,
#             month=12,
#             content_type='application/x-markdown',
#             schema_name='article'
#         )
#         c.new_revision(metadata={
#             'title': 'Test Article',
#             'author': 'Johan Bach'
#         })


#     def test_no_fields_given(self):
#         url = reverse('autocomplete-components', kwargs={

#         })
#         self.fail('not yet implemented')

#     def test_blank_field_given(self):
#         self.fail('not yet implemented')

#     def test_no_query_given(self):
#         self.fail('not yet implemented')

#     def testnn_no_schema_type_given(self):
#         self.fail('not yet implemented')

#     def test_no_such_schema_type(self):
#         # There are results by virtue of fields and q, but none by the schema
#         # type
#         self.fail('not yet implemented')

#     def test_no_such_q(self):
#         # There are results by virtue of the schema types, but none that
#         # contain the value of q in the given fields
#         self.fail('not yet implemented')

#     def test_q_too_short(self):
#         self.fail('not yet implemented')

#     def test_case_insensitivity(self):
#         self.fail('not yet implemented')


# class AutocompleteURLsTest(TestCase):
#     def test_url_preset(self):
#         self.fail('not yet implemented')
