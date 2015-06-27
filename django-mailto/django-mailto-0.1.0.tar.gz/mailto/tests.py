# -*- coding: utf-8 -*-
from urlparse import urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core import mail
from django.test import TestCase, Client
import mock

from mailto import mailto
from mailto.models import UserOptin, Mail


class OptinCreationTest(TestCase):

    def setUp(self):
        self.user0 = User.objects.create(username='test0')
        self.user1 = User.objects.create(username='test1')
        self.client = Client()

    def test_has_optin(self):
        self.assertIsInstance(self.user0.optin, UserOptin)
        self.assertTrue(self.user0.optin.optin)

        self.assertIsInstance(self.user1.optin, UserOptin)
        self.assertTrue(self.user1.optin.optin)


class MailtoNewMailTest(TestCase):

    def test_mailto_empty(self):
        self.assertIsNone(mailto([], 'test'))
        self.assertRaises(TypeError, mailto(None, 'test'))

    def test_mailto_with_new_mail(self):
        mailto(['test@localhost'], 'test')

        email = Mail.objects.get(slug='test', language_code=settings.LANGUAGE_CODE)

        self.assertIsNotNone(email)

        self.assertFalse(email.active)
        self.assertEqual(email.slug, 'test')
        self.assertEqual(email.language_code, settings.LANGUAGE_CODE)
        self.assertIsNotNone(email.template)

        self.assertIsNotNone(email.sender_email)
        self.assertIsNone(email.sender_name)
        self.assertIsNone(email.reply_to)
        self.assertIsNone(email.cc)
        self.assertIsNone(email.bcc)

        self.assertEqual(email.subject, 'test')
        self.assertEqual(email.plain, 'test')
        self.assertIsNone(email.html)

        self.assertTrue(email.optout)

    def test_malto_with_new_mail_not_sent(self):
        self.assertEqual(len(mail.outbox), 0)


class MailtoTest(TestCase):

    def setUp(self):
        self.site = Site.objects.create(domain='localhost', name='localhost')
        self.user = User.objects.create(username='test', email='test@localhost')
        mailto(['test@localhost'], 'test')
        self.mail = Mail.objects.get(slug='test', language_code=settings.LANGUAGE_CODE)

    def test_send_inactive(self):
        self.mail.active = False
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 0)

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_active(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_active_html(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True

        # test invalid html
        self.mail.html = 'test html'
        self.mail.save()

        with self.assertRaises(ValueError):
            mailto(['test@localhost'], 'test')
        self.assertEqual(len(mail.outbox), 0)

        # test empty object
        self.mail.html = None
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

        # test empty object
        self.mail.html = '{}'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[1].subject, 'test')
        self.assertEqual(mail.outbox[1].body, 'test')
        self.assertEqual(mail.outbox[1].to, ['test@localhost'])
        self.assertEqual(mail.outbox[1].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[1].cc, [])
        self.assertEqual(mail.outbox[1].bcc, [])
        self.assertEqual(mail.outbox[1].alternatives, [])
        self.assertEqual(mail.outbox[1].extra_headers, {})

        # test valid html
        self.mail.html = '{"foo": "bar"}'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 3)
        self.assertEqual(mail.outbox[2].subject, 'test')
        self.assertEqual(mail.outbox[2].body, 'test')
        self.assertEqual(mail.outbox[2].to, ['test@localhost'])
        self.assertEqual(mail.outbox[2].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[2].cc, [])
        self.assertEqual(mail.outbox[2].bcc, [])
        self.assertEqual(len(mail.outbox[2].alternatives), 1)
        self.assertEqual(mail.outbox[2].extra_headers, {})

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_active_with_optin(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.save()

        self.user.optin.optin = True
        self.user.optin.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_inactive_with_optin(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = False
        self.mail.save()

        self.user.optin.optin = True
        self.user.optin.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 0)

    def test_send_active_with_optout(self):
        self.mail.active = True
        self.mail.save()

        self.user.optin.optin = False
        self.user.optin.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 0)

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_cc_recipients(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.cc = 'cc1@localhost, cc2@localhost,cc3@localhost'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, ['cc1@localhost', 'cc2@localhost', 'cc3@localhost'])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_bcc_recipients(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.bcc = 'bcc1@localhost, bcc2@localhost,bcc3@localhost'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, ['bcc1@localhost', 'bcc2@localhost', 'bcc3@localhost'])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_reply_to(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.reply_to = 'noreply@localhost'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, settings.DEFAULT_FROM_EMAIL)
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {
            'Reply-To': 'noreply@localhost'
        })

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_email_address_with_name(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.sender_name = 'John Doe'
        self.mail.save()

        mailto(['test@localhost'], 'test')

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, 'test')
        self.assertEqual(mail.outbox[0].body, 'test')
        self.assertEqual(mail.outbox[0].to, ['test@localhost'])
        self.assertEqual(mail.outbox[0].from_email, '%s <%s>' % ('John Doe', settings.DEFAULT_FROM_EMAIL))
        self.assertEqual(mail.outbox[0].cc, [])
        self.assertEqual(mail.outbox[0].bcc, [])
        self.assertEqual(mail.outbox[0].alternatives, [])
        self.assertEqual(mail.outbox[0].extra_headers, {})

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_email_with_kwargs(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.reply_to = 'noreply@localhost'
        self.mail.cc = 'cc@localhost'
        self.mail.bcc = 'bcc@localhost'
        self.mail.save()

        mailto(['test@localhot'], 'test', **{
            'from_email': 'from@localhost',
            'cc': ['cc1@localhost', 'cc2@localhost'],
            'bcc': ['bcc1@localhost', 'bcc2@localhost'],
            'reply_to': 'reply-to@localhost',
            'headers': {
                'header1': 'header_value_1',
            },
            'attachments': [('mail.js', '/static/js/mail.js', 'text/javascript')]
        })

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].from_email, 'from@localhost')
        self.assertEqual(mail.outbox[0].cc, ['cc@localhost', 'cc1@localhost', 'cc2@localhost'])
        self.assertEqual(mail.outbox[0].bcc, ['bcc@localhost', 'bcc1@localhost', 'bcc2@localhost'])
        self.assertEqual(mail.outbox[0].extra_headers.get('header1'), 'header_value_1')
        self.assertEqual(mail.outbox[0].extra_headers.get('Reply-To'), 'reply-to@localhost')
        self.assertEqual(mail.outbox[0].attachments, [('mail.js', '/static/js/mail.js', 'text/javascript')])

    @mock.patch('django.contrib.sites.models.Site.objects.get_current')
    def test_send_email_indiviual_mail(self, mock_get_current):
        mock_get_current.return_value = self.site
        self.mail.active = True
        self.mail.plain = 'Hello {{ recipient.email }}'
        self.mail.save()

        user2 = User.objects.create(username='test2', email='test2@localhost')

        mailto(['test@localhost', 'test2@localhost', ], 'test')

        self.assertIs(len(mail.outbox), 2)

        self.assertIn(user2.email, mail.outbox[0].body)
        self.assertEqual(mail.outbox[0].to, [user2.email])

        self.assertIn(self.user.email, mail.outbox[1].body)
        self.assertEqual(mail.outbox[1].to, [self.user.email])