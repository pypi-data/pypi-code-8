# import time
# 
# from selenium.webdriver.firefox.webdriver import WebDriver
# from selenium.webdriver.common.keys import Keys
# 
# from django.test import LiveServerTestCase
# from django.contrib.auth.models import User
# 
# from edc.testing.models import TestM2m, TestForeignKey, TestModel
# 
# 
# class TestSelenium(LiveServerTestCase):
# 
#     def setUp(self):
#         self.adminuser = User.objects.create_user('django', 'django@test.com', 'pass')
#         self.adminuser.save()
#         self.adminuser.is_staff = True
#         self.adminuser.is_active = True
#         self.adminuser.is_superuser = True
#         self.adminuser.save()
#         self.logged_in = False
#         self.login()
#         TestM2m.objects.create(name='test_m2m1', short_name='test_m2m1')
#         TestM2m.objects.create(name='test_m2m2', short_name='test_m2m2')
#         TestM2m.objects.create(name='test_m2m3', short_name='test_m2m3')
#         TestForeignKey.objects.create(name='test_fk', short_name='test_fk')
#         #self.survey = "MPP Year 1"
# 
#     @classmethod
#     def setUpClass(cls):
#         cls.selenium = WebDriver()
#         super(TestsSelenium, cls).setUpClass()
# 
#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super(TestsSelenium, cls).tearDownClass()
# 
#     def login(self):
#         self.selenium.get('%s%s' % (self.live_server_url, '/erik/'))
#         self.selenium.get('%s%s' % (self.live_server_url, '/login/'))
#         username_input = self.selenium.find_element_by_name("username")
#         username_input.send_keys('django')
#         password_input = self.selenium.find_element_by_name("password")
#         password_input.send_keys('pass')
#         self.selenium.find_element_by_xpath('//input[@value="Log in"]').click()
#         self.selenium.get('%s%s' % (self.live_server_url, '/admin/testing'))
#         self.logged_in = True
# 
#     def test_test_model(self):
#         self.selenium.find_element_by_xpath('//input[@value="Administration"]').click()
#         self.selenium.find_element_by_xpath('//input[@value="Site Admin"]').click()
#         self.selenium.find_element_by_xpath('//a[@href="/admin/testing/testmodel/add/"]').click()
#         fld = self.selenium.find_element_by_name("name")
#         fld.send_keys('TEST')
#         fld = self.selenium.find_element_by_name("test_foreign_key")
#         fld.send_keys(Keys.ARROW_DOWN)
#         fld = self.selenium.find_element_by_name("test_many_to_many")
#         fld.send_keys(Keys.ARROW_RIGHT)
#         fld.send_keys(Keys.ARROW_DOWN)
#         self.selenium.find_element_by_xpath('//input[@value="Save"]').click()
#         pk = TestModel.objects.all()[0].pk
#         self.selenium.find_element_by_xpath('//a[@href="{0}/"]'.format(pk)).click()
#         self.assertEqual([test_many_to_many.name for test_many_to_many in TestModel.objects.get(pk=pk).test_many_to_many.all()], ['test_m2m2'])
#         time.sleep(5)
