from mock import patch

import responses
from django.test import TestCase
from django.test.utils import override_settings

from mgsub.mailgun import MailgunList, MailgunError


@override_settings(MGSUB_DEFAULT_MAILINGLIST='list@example.com')
class MailinglistTestCase(TestCase):

    def test_list_url(self):
        mailinglist = MailgunList()
        url = mailinglist.get_list_url()
        exp = 'https://api.mailgun.net/v2/lists/list@example.com/members'
        self.assertEquals(url, exp)

    def test_explicit_list_url(self):
        with patch.dict('os.environ', {'MGSUB_DEFAULT_MAILINGLIST':
                                       'list3@example.com'}, clear=True):
            mailinglist = MailgunList('list2@example.com')
            url = mailinglist.get_list_url()
            exp = 'https://api.mailgun.net/v2/lists/list2@example.com/members'
            self.assertEquals(url, exp)

    @override_settings(MGSUB_DEFAULT_MAILINGLIST=None)
    def test_env_list_url(self):
        with patch.dict('os.environ', {'MGSUB_DEFAULT_MAILINGLIST':
                                       'list3@example.com'}, clear=True):
            mailinglist = MailgunList()
            url = mailinglist.get_list_url()
            exp = 'https://api.mailgun.net/v2/lists/list3@example.com/members'
            self.assertEquals(url, exp)

    def test_api_key(self):
        with patch.dict('os.environ', {}, clear=True):
            mailinglist = MailgunList()
            self.assertIsNone(mailinglist.api_key)

    def test_api_environ(self):
        with patch.dict('os.environ', {'MAILGUN_API_KEY': 'env'}):
            mailinglist = MailgunList()
            self.assertEqual(mailinglist.api_key, 'env')

    @override_settings(MAILGUN_API_KEY='settings')
    def test_api_settings(self):
        mailinglist = MailgunList()
        self.assertEqual(mailinglist.api_key, 'settings')

    def test_member_url(self):
        mailinglist = MailgunList()
        url = mailinglist.get_member_url('sample@example.com')
        self.assertIn('list@example.com/members/sample@example.com', url)

    @responses.activate
    def test_subscribe_success(self):
        resp = \
            '''{
                 "member": {
                   "vars": {
                     "age": 26
                   },
                   "name": "Bob Bar",
                   "subscribed": true,
                   "address": "bar@example.com"
                 },
                 "message": "Mailing list member has been created"
            }'''
        url = 'https://api.mailgun.net/v2/lists/list@example.com/members'
        responses.add(responses.POST, url,
                      resp, content_type='application/json')

        mailinglist = MailgunList()
        result = mailinglist.subscribe('bob@example.com', 'Bob Bar')
        self.assertEquals(result['member']['address'], 'bar@example.com')

    @responses.activate
    def test_unsubscribe_success(self):
        resp = \
            '''{
                 "member":
                   {
                     "address": "bar@example.com"
                   },
                   "message": "Mailing list member has been deleted"
               }'''
        url = 'https://api.mailgun.net/v2/lists/list@example.com/members/bob@example.com'
        responses.add(responses.DELETE, url,
                      resp, content_type='application/json')

        mailinglist = MailgunList()
        result = mailinglist.unsubscribe('bob@example.com')
        self.assertEquals(result['member']['address'], 'bar@example.com')

    @responses.activate
    def test_subscribe_duplicate(self):
        resp = \
            '''{
                 "message": "Address already exists"
               }'''
        url = 'https://api.mailgun.net/v2/lists/list@example.com/members'
        responses.add(responses.POST, url,
                      resp, content_type='application/json',
                      status=400,
                      adding_headers={'content-length': str(len(resp))})

        mailinglist = MailgunList()
        result = mailinglist.subscribe('bob@example.com', 'Bob Bar')
        self.assertEquals(result['member']['address'], 'bob@example.com')

    @responses.activate
    def test_subscribe_400(self):
        resp = \
            '''{
                 "message": "Bad request"
               }'''
        url = 'https://api.mailgun.net/v2/lists/list@example.com/members'
        responses.add(responses.POST, url,
                      resp, content_type='application/json',
                      status=400,
                      adding_headers={'content-length': str(len(resp))})

        mailinglist = MailgunList()
        with self.assertRaises(MailgunError) as cm:
            mailinglist.subscribe('bob@example.com', 'Bob Bar')
        self.assertEqual(400, cm.exception.code)
        self.assertEqual('Bad request', cm.exception.json['message'])

    @responses.activate
    def test_unsubscribe_400(self):
        resp = \
            '''{
                 "message": "Bad request"
               }'''
        url = 'https://api.mailgun.net/v2/lists/list@example.com/members/bob@example.com'
        responses.add(responses.DELETE, url,
                      resp, content_type='application/json',
                      status=400,
                      adding_headers={'content-length': str(len(resp))})

        mailinglist = MailgunList()
        with self.assertRaises(MailgunError) as cm:
            mailinglist.unsubscribe('bob@example.com')

        self.assertEqual(400, cm.exception.code)
        self.assertEqual('Bad request', cm.exception.json['message'])
