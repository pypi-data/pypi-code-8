from datetime import datetime
from unittest import TestCase

import mock

from unicore.comments.client.tests import fixtures as f
from unicore.comments.client import Comment, CommentClient


class CommentTestCase(TestCase):

    def setUp(self):
        self.client = mock.Mock(spec=CommentClient)
        self.comment = Comment(self.client, f.comment_data.copy())

    def test_coerce_fields(self):
        self.assertIsInstance(self.comment.data['submit_datetime'], datetime)
        self.assertIsInstance(self.comment.data['flag_count'], int)
        self.assertIsInstance(self.comment.data['is_removed'], bool)

    def test_set(self):
        self.assertRaisesRegexp(
            ValueError, 'cannot be set', self.comment.set, 'uuid', 'value')
        self.comment.set('comment', 'foo')
        self.assertEqual(self.comment.data.get('comment'), 'foo')

    def test_get(self):
        self.assertEqual(
            self.comment.get('user_uuid'), f.comment_data['user_uuid'])

    def test_flag(self):
        user_uuid = f.flag_data['user_uuid']
        self.client.create_flag.return_value = True
        self.comment.flag(user_uuid)

        data_arg = self.client.create_flag.call_args[0][0]
        self.assertDictContainsSubset({
            'app_uuid': self.comment.get('app_uuid'),
            'comment_uuid': self.comment.get('uuid'),
            'user_uuid': user_uuid}, data_arg)
        self.assertIsInstance(data_arg.get('submit_datetime'), basestring)
        self.assertEqual(self.comment.get('flag_count'), 1)

        self.client.create_flag.return_value = False
        self.comment.flag(user_uuid)

        self.assertEqual(self.comment.get('flag_count'), 1)

    def test_unflag(self):
        user_uuid = f.flag_data['user_uuid']
        self.client.delete_flag.return_value = True
        self.comment.unflag(user_uuid)

        self.client.delete_flag.assert_called_with(
            self.comment.get('uuid'), user_uuid)
        self.assertEqual(self.comment.get('flag_count'), -1)

        self.client.delete_flag.return_value = False
        self.comment.unflag(user_uuid)

        self.assertEqual(self.comment.get('flag_count'), -1)
