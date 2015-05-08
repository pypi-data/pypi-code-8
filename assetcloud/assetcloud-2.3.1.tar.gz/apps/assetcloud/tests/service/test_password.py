# -*- coding: utf-8 -*-
# (c) 2011 Bright Interactive Limited. All rights reserved.
# http://www.bright-interactive.com | info@bright-interactive.com

from assetcloud.tests.service.utils import TestCase, create_user
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class PasswordPageTests(TestCase):
    """
    Page tests for changing users' passwords.
    """

    def test_change_password(self):
        initial_password = 'mvsX3HFg'
        new_password = 'yF6ACiwD'

        user = create_user(password=initial_password)

        response = self.post_change_password_request(
            user, initial_password, new_password)

        self.assertEquals(response.status_code, 200)

        # check that password has been changed to new_password and that
        # initial_password is no longer accepted
        user = User.objects.get(id=user.id)
        self.assertFalse(user.check_password(initial_password))
        self.assertTrue(user.check_password(new_password))

    def test_passwords_dont_match_password_not_changed(self):
        initial_password = 'mvsX3HFg'
        new_password = 'yF6ACiwD'

        user = create_user(password=initial_password)

        response = self.post_change_password_request(
            user, initial_password, new_password, new_password + 'mistake')

        self.assertEquals(response.status_code, 200)

        # check that password has not been changed to new_password and that
        # initial_password is still accepted
        user = User.objects.get(id=user.id)
        self.assertTrue(user.check_password(initial_password))
        self.assertFalse(user.check_password(new_password))

    def test_post_forgotten_password_where_user_does_not_exist(self):
        user = create_user()

        form_data = {'email': "invalid-user" + user.email}
        response = self.client.post(reverse('forgotten-password'),
            form_data, follow=True)

        self.assertFormError(response, 'form', 'email', 'No user with this email exists.')

    def test_post_forgotten_password_where_user_is_deleted(self):
        user = create_user(is_active=False)

        form_data = {'email': user.email}
        response = self.client.post(reverse('forgotten-password'),
            form_data, follow=True)

        self.assertFormError(response, 'form', 'email', 'This account has been deleted.')

    def test_post_forgotten_password_where_user_is_pending(self):
        user = create_user(is_active=False, has_activation_key=True)

        form_data = {'email': user.email}
        response = self.client.post(reverse('forgotten-password'),
            form_data, follow=True)

        self.assertFormError(response, 'form', 'email', 'This account is pending activation.')

    def post_change_password_request(self, user, initial_password,
                                     new_password1, new_password2=None):
        if not new_password2:
            new_password2 = new_password1

        self.client.login(user)

        form_data = {
            'old_password': initial_password,
            'new_password1': new_password1,
            'new_password2': new_password2,
        }
        response = self.client.post(reverse('change-password'),
                                    form_data, follow=True)
        return response

    def test_section(self):
        """
        Make sure that the correct `section` ends up in the template context so
        that nav.html highlights the correct section (users).
        """
        user = create_user()
        self.client.login(user)

        response = self.client.post(reverse('change-password'))
        # check it's not a redirect
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['section'], 'users')

    def test_social_auth_users_cant_see_change_password(self):
        user = create_user(social_auth=True)
        self.client.login(user)
        response = self.client.get(reverse('home'), follow=True)
        self.assertNotIn('Change password', response.content)
