# from django.contrib import admin
# from django.contrib.auth.models import User
# from django.core.urlresolvers import reverse
# from django.http import HttpResponseRedirect
# from django.test import TestCase
# from django.test.client import RequestFactory
# 
# from ..modeladmin import NextUrlError
# 
# from .models import TestModel
# 
# 
# class TestAdmin(TestCase):
# 
#     urls = "urls"
# 
#     def setUp(self):
#         self.factory = RequestFactory()
#         self.user = self._create_superuser('django')
#         # self.test_model = TestModelFactory()
# 
#     def _create_superuser(self, username):
#         return User.objects.create(username=username, is_superuser=True)
# 
#     def _mocked_authenticated_request(self, url, user):
#         request = self.factory.get(url)
#         request.user = user
#         return request
# 
#     def test_redirect1(self):
#         """Asserts raises exception if specify next=add with missing GET parameters"""
#         test_model = TestModel()
#         test_model_admin = admin.site._registry.get(TestModel)
#         url = reverse('admin:testing_testmodel_add')
#         app_label, module_name = None, None
#         url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
#         request = self._mocked_authenticated_request(url, self.user)
#         next_url_name = 'add'
#         self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)
# 
#     def test_redirect2(self):
#         app_label, module_name = 'testing', None
#         url = reverse('admin:testing_testmodel_add')
#         next_url_name = 'add'
#         test_model = TestModel()
#         test_model_admin = admin.site._registry.get(TestModel)
#         url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
#         request = self._mocked_authenticated_request(url, self.user)
#         self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)
# 
#     def test_redirect3(self):
#         test_model = TestModel()
#         test_model_admin = admin.site._registry.get(TestModel)
#         url = reverse('admin:testing_testmodel_add')
#         app_label, module_name = 'testing', 'testmodel'
#         next_url_name = 'add'
#         url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
#         request = self._mocked_authenticated_request(url, self.user)
#         self.assertTrue(isinstance(test_model_admin.response_add_redirect_on_next_url(next_url_name, request, test_model, None), HttpResponseRedirect))
# 
#     def test_redirect4(self):
#         test_model = TestModel()
#         test_model_admin = admin.site._registry.get(TestModel)
#         next_url_name = 'changelist'
#         url = reverse('admin:testing_testmodel_changelist')
#         app_label, module_name = None, None
#         url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
#         request = self._mocked_authenticated_request(url, self.user)
#         self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)
# 
#     def test_redirect5(self):
#         test_model = TestModel()
#         test_model_admin = admin.site._registry.get(TestModel)
#         next_url_name = 'changelist'
#         url = reverse('admin:testing_testmodel_changelist')
#         app_label, module_name = 'testing', None
#         url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
#         request = self._mocked_authenticated_request(url, self.user)
#         self.assertRaises(NextUrlError, test_model_admin.response_add_redirect_on_next_url, next_url_name, request, test_model, None)
# 
#     def test_redirect6(self):
#         test_model = TestModel()
#         test_model_admin = admin.site._registry.get(TestModel)
#         next_url_name = 'changelist'
#         url = reverse('admin:testing_testmodel_changelist')
#         app_label, module_name = 'testing', 'testmodel'
#         url = '{0}?next=add&app_label={1}&module_name={2}'.format(url, app_label or '', module_name or '')
#         request = self._mocked_authenticated_request(url, self.user)
#         self.assertTrue(isinstance(test_model_admin.response_add_redirect_on_next_url(next_url_name, request, test_model, None), HttpResponseRedirect))
