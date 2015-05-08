# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.conf import settings
from django.test.utils import override_settings
from assetcloud.tests.contract.utils import ContractTest

from assetcloud.tests.service.utils import TestCase, create_user, create_fake_request
from django.core.urlresolvers import reverse
from django.contrib import messages
import assetcloud_auth


class LoginTests(TestCase):
    """
    Service tests for authentication, logging in and logging out.
    """

    def test_login_exists(self):
        """
        Ensure the login page exists.
        """
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'assetcloud/pages/logged_out/login.html')

    def test_logout_exists(self):
        """
        Ensure the logout view exists.
        """
        self.client.login()
        response = self.client.get(reverse('logout'), follow=True)
        self.assertEquals(response.status_code, 200)

    @ContractTest(app="tnabot")
    @override_settings(LOGOUT_REDIRECT_URL=reverse('register'))
    def test_logout_redirects_to_setting(self):
        self.client.login()
        response = self.client.get(reverse('logout'), follow=True)
        self.assertRedirects(response, settings.LOGOUT_REDIRECT_URL)

    def test_pages_require_login(self):
        """
        Ensure that the front pages in asset cloud redirect the user
        to the login page if the user is not logged in.
        """
        for page in ['home', 'asset-list', 'asset-upload', 'account-users',
                     'customise-account']:
            response = self.client.get(reverse(page), follow=True)
            self.assertEquals(response.status_code, 200)
            self.assertTemplateUsed(response, 'assetcloud/pages/logged_out/login.html')

    def assertMessageQueueEmpty(self, request):
        self.assertEqual(len(messages.get_messages(request)), 0)

    def assertMessageQueueNotEmpty(self, request):
        self.assertNotEqual(len(messages.get_messages(request)), 0)

    def test_notify_login_error_message_works_for_not_fully_registered(self):
        request = create_fake_request(create_user(email=''))
        self.assertFalse(request.user.get_profile().is_registered)
        self.assertMessageQueueEmpty(request)
        assetcloud_auth.notify_login_error_message(request, request.user)
        self.assertMessageQueueNotEmpty(request)

    def test_notify_login_error_message_works_for_deactivated(self):
        request = create_fake_request(create_user(is_active=False,
                                                  has_activation_key=False))
        self.assertTrue(request.user.get_profile().is_deleted)
        self.assertMessageQueueEmpty(request)
        assetcloud_auth.notify_login_error_message(request, request.user)
        self.assertMessageQueueNotEmpty(request)

    def test_notify_login_error_message_works_for_pending(self):
        request = create_fake_request(create_user(is_active=False,
                                                  has_activation_key=True))
        self.assertTrue(request.user.get_profile().is_pending)
        self.assertMessageQueueEmpty(request)
        assetcloud_auth.notify_login_error_message(request, request.user)
        self.assertMessageQueueNotEmpty(request)
