from unittest import TestCase
from copy import deepcopy

import mock

from unicore.comments.client.tests import fixtures as f
from unicore.comments.client import (
    CommentPage, CommentClient, Comment, LazyCommentPage)


class CommentPageTestCase(TestCase):

    def setUp(self):
        self.client = mock.Mock(spec=CommentClient)
        self.page = CommentPage(self.client, deepcopy(f.comment_stream_data))

    def test_properties(self):
        self.assertEqual(self.page.start, f.comment_stream_data['start'])
        self.assertEqual(self.page.end, f.comment_stream_data['end'])
        self.assertEqual(self.page.total, f.comment_stream_data['total'])
        self.assertEqual(self.page.metadata, f.comment_stream_data['metadata'])
        self.assertEqual(
            self.page.state, f.comment_stream_data['metadata']['state'])

    def test_iterable(self):
        length = len(self.page)
        self.assertEqual(length, f.comment_stream_data['count'])

        for i, comment in enumerate(self.page):
            self.assertIsInstance(comment, Comment)
        self.assertEqual(i, length - 1)

    def test_previous(self):
        self.assertTrue(self.page.has_previous())

        self.page.data['start'] = 0
        self.assertFalse(self.page.has_previous())

        self.page.data['start'] = 20
        self.page.data['total'] = 0
        self.assertFalse(self.page.has_previous())

        self.page.data['total'] = 100
        first_obj = f.comment_stream_data['objects'][0]
        self.assertEqual(
            self.page.get_previous_args(),
            {'after': first_obj['uuid'],
             'app_uuid': first_obj['app_uuid'],
             'content_uuid': first_obj['content_uuid']})

    def test_next(self):
        self.assertTrue(self.page.has_next())

        self.page.data['end'] = self.page.data['total']
        self.assertFalse(self.page.has_next())

        self.page.data['end'] = 30
        self.page.data['total'] = 0
        self.assertFalse(self.page.has_next())

        self.page.data['total'] = 100
        last_obj = f.comment_stream_data['objects'][-1]
        self.assertEqual(
            self.page.get_next_args(),
            {'before': last_obj['uuid'],
             'app_uuid': last_obj['app_uuid'],
             'content_uuid': last_obj['content_uuid']})


class LazyCommentPageTestCase(CommentPageTestCase):

    def setUp(self):
        super(LazyCommentPageTestCase, self).setUp()
        self.client.get_comment_page.return_value = self.page
        self.page = LazyCommentPage(
            self.client,
            limit=10,
            app_uuid=f.comment_data['app_uuid'],
            content_uuid=f.comment_data['content_uuid'])

    def test_lazy_loading(self):
        self.assertIs(self.page._data, None)
        self.client.get_comment_page.assert_not_called()

        self.assertTrue(self.page.data)
        self.assertTrue(self.page._data)
        self.client.get_comment_page.assert_called_with(
            app_uuid=f.comment_data['app_uuid'],
            content_uuid=f.comment_data['content_uuid'],
            limit=10)

        self.client.get_comment_page.reset_mock()
        self.assertTrue(self.page.data)
        self.client.get_comment_page.assert_not_called()
