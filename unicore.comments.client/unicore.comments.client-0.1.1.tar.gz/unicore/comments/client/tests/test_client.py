import re
import json
from unittest import TestCase
from uuid import uuid4
from urlparse import urlparse, parse_qs

import responses

from unicore.comments.client import (
    CommentClient, CommentPage, Comment, UserBanned, CommentStreamNotOpen)
from unicore.comments.client.tests import fixtures as f


class BaseClientTestMixin(object):

    @classmethod
    def setUpClass(cls):
        cls.app_id = uuid4().hex
        cls.host = 'http://localhost:8000'
        cls.client = cls.client_class(host=cls.host)

    def check_request_basics(self, url):
        self.assertEqual(len(responses.calls), 1)
        request = responses.calls[0].request
        r_url = urlparse(request.url)
        url = urlparse(url)
        self.assertEqual(r_url[:4], url[:4])
        self.assertEqual(parse_qs(r_url.query), parse_qs(url.query))

    def test_from_config(self):
        settings = {
            'unicorecomments.host': 'http://localhost:8080',
        }
        client = self.client_class.from_config(settings)
        self.assertEqual(client.settings, {
            'host': settings['unicorecomments.host']})


class CommentClientTestCase(BaseClientTestMixin, TestCase):
    client_class = CommentClient

    @responses.activate
    def test_get_comment_page(self):
        responses.add(
            responses.GET, re.compile(r'.*/comments/.*'),
            f.comment_stream_json, status=200, content_type='application/json')
        page = self.client.get_comment_page(
            'app_uuid', 'content_uuid', after='after_uuid',
            limit=100, offset=20, before='before_uuid')

        self.assertIsInstance(page, CommentPage)
        self.check_request_basics(
            url='%s/comments/?after=after_uuid&before=before_uuid&'
                'app_uuid=app_uuid&content_uuid=content_uuid&'
                'limit=100&offset=20' % self.host)

    @responses.activate
    def test_create_comment(self):
        url_regex = re.compile(r'.*/comments/.*')
        responses.add(
            responses.POST, re.compile(r'.*/comments/.*'), f.comment_json,
            status=201, content_type='application/json')
        comment = self.client.create_comment({})

        self.assertIsInstance(comment, Comment)
        self.check_request_basics(url='%s/comments/' % self.host)

        for error_code, error_cls in (
                ('USER_BANNED', UserBanned),
                ('STREAM_NOT_OPEN', CommentStreamNotOpen)):
            error_data = f.generic_error_data.copy()
            error_data['error_code'] = error_code
            responses.reset()
            responses.add(
                responses.POST, url_regex, json.dumps(error_data),
                status=403, content_type='application/json')

            self.assertRaises(error_cls, self.client.create_comment, {})

    @responses.activate
    def test_create_flag(self):
        url_regex = re.compile(r'.*/flags/.*')
        responses.add(
            responses.POST, url_regex, f.flag_json,
            status=201, content_type='application/json')
        result = self.client.create_flag({})

        self.assertTrue(result)
        self.check_request_basics(url='%s/flags/' % self.host)

        responses.reset()
        responses.add(
            responses.POST, url_regex, f.flag_json,
            status=200, content_type='application/json')
        result = self.client.create_flag({})

        self.assertFalse(result)

    @responses.activate
    def test_delete_flag(self):
        url_regex = re.compile(r'.*/flags/.*')
        responses.add(
            responses.DELETE, url_regex, f.flag_json,
            status=200, content_type='application/json')
        result = self.client.delete_flag('comment_uuid', 'user_uuid')

        self.assertTrue(result)
        self.check_request_basics(
            url='%s/flags/comment_uuid/user_uuid/' % self.host)

        responses.reset()
        responses.add(
            responses.DELETE, url_regex, f.generic_error_json,
            status=404, content_type='application/json')
        result = self.client.delete_flag('comment_uuid', 'user_uuid')

        self.assertFalse(result)
