# (c) 2011-2013 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com
from django.conf import settings
from assetcloud.models import get_user_profile_class
from assetcloud.tests.service.utils import TestCase, create_organisation_type, get_last_added_user, get_last_added_account, create_user
from assetcloud import random_utils
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse

UserProfile = get_user_profile_class()


class RegisterTests(TestCase):
    def setUp(self):
        super(RegisterTests, self).setUp()
        self.data = self.create_valid_register_data()

    def tearDown(self):
        super(RegisterTests, self).tearDown()

    def create_valid_register_data(self):
        d = {}
        d['email'] = random_utils.random_email()
        d['org_type'] = create_organisation_type().pk
        d['org_name'] = random_utils.random_alphanumeric()
        return d

    def test_register_page_requires_email(self):
        del self.data['email']
        response = self.submit_register_form(**self.data)
        self.assertContains(response, 'This field is required')

    def test_register_page_does_not_require_password(self):
        response = self.submit_register_form(**self.data)
        self.assertNotContains(response, 'This field is required')

    def test_register_page_redirects_to_activation_sent(self):
        response = self.submit_valid_register_form()
        self.assertTemplateUsed(response, 'assetcloud/pages/registration/activation_sent.html')

    def test_register_page_creates_inactive_user(self):
        self.submit_valid_register_form()
        user = get_last_added_user()
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, self.data['email'])
        self.assertFalse(authenticate(username=user.email, password=user.password))
        self.assertFalse(authenticate(username=user.email, password=''))

    def test_register_page_creates_account(self):
        self.submit_valid_register_form()
        account = get_last_added_account()
        self.assertEqual(account.name, self.data['org_name'])
        self.assertEqual(account.organisation_type.pk, self.data['org_type'])

    def test_register_page_creates_account_and_user(self):
        self.submit_valid_register_form()
        account = get_last_added_account()
        user = get_last_added_user()
        self.assertEqual(account, user.get_profile().account)

    def test_register_page_sends_activation_key(self):
        self.assertEqual(len(mail.outbox), 0)
        self.submit_valid_register_form()
        self.assertEqual(len(mail.outbox), 1)
        # Todo: test for key in email - encoding seems to mess it up

    def test_register_page_prompts_for_password_on_activation(self):
        self.submit_valid_register_form()
        user = get_last_added_user()
        self.assertFalse(user.get_profile().is_active)
        response = self.client.get(
            reverse('activate-user', kwargs={
                'key': user.get_profile().activation_key}),
            follow=True)
        user = User.objects.get(pk=user.pk)
        self.assertFalse(user.get_profile().is_active)
        self.assertContains(response, 'id="id_new_password1"')

    def submit_register_form(self, email=None, org_name=None, org_type=None):
        data = {}
        if email:
            data['email'] = email
        if org_name:
            data['name'] = org_name
        if org_type:
            data['organisation_type'] = org_type
        return self.client.post(reverse('register'), data, follow=True)

    def submit_valid_register_form(self):
        self.data = self.create_valid_register_data()
        return self.submit_register_form(**self.data)

    def test_register_page_exists(self):
        response = self.client.get(reverse('register'))
        self.assertTemplateUsed(response, 'assetcloud/pages/registration/register.html')

    def test_register_page_asks_for_email(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'Email')
        self.assertContains(response, 'id="id_email"')

    def test_register_page_does_not_ask_for_password(self):
        response = self.client.get(reverse('register'))
        self.assertNotContains(response, 'Password')
        self.assertNotContains(response, 'id="id_password"')

    def test_register_page_asks_for_org_name(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'Organisation name')
        self.assertContains(response, 'id="id_name"')

    def test_register_page_asks_for_org_type(self):
        response = self.client.get(reverse('register'))
        self.assertContains(response, 'Organisation type')
        self.assertContains(response, 'id="id_organisation_type"')

    def test_register_page_does_not_require_org_name(self):
        del self.data['org_name']
        response = self.submit_register_form(**self.data)
        self.assertNotContains(response, 'This field is required')

    def test_register_page_does_not_require_org_type(self):
        del self.data['org_type']
        response = self.submit_register_form(**self.data)
        self.assertNotContains(response, 'This field is required')

    def submit_social_register_form(self, **data):
        user = create_user(social_auth=True, has_activation_key=True,
                           is_active=False)
        return self.client.post(
            reverse('complete_profile_action',
                    kwargs={'user_id': user.id,
                            'key': user.get_profile().activation_key}),
            data, follow=True)

    def test_social_auth_users_activate_immediately(self):
        self.submit_social_register_form(**self.data)
        user = get_last_added_user()
        response = self.client.get(reverse('activate-user', kwargs={'key': user.get_profile().activation_key}), follow=True)
        self.assertRedirects(response, str(settings.LOGIN_REDIRECT_URL))

    def get_social_auth_response(self):
        user = create_user(social_auth=True, is_active=False, email='',
                           has_activation_key=True)
        return self.client.get(
            reverse('complete_profile_action',
                    kwargs={'user_id': user.id,
                            'key': user.get_profile().activation_key}))

    def test_social_auth_page_does_not_require_password(self):
        response = self.get_social_auth_response()
        self.assertNotContains(response, 'Password')
        self.assertNotContains(response, 'password="id_password"')

    def test_social_auth_page_requires_email(self):
        response = self.get_social_auth_response()
        self.assertContains(response, 'Email')
        self.assertContains(response, 'id="id_email"')
