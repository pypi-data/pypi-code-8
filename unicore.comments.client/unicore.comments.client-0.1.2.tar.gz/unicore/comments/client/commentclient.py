import json
from datetime import datetime
import pytz
from dateutil.parser import parse as parse_dt

from unicore.comments.client.base import (
    BaseClient, BaseClientObject, CommentServiceException)


class UserBanned(CommentServiceException):
    pass


class CommentStreamNotOpen(CommentServiceException):
    pass


class CommentClient(BaseClient):
    base_path = '/comments/'

    def get_comment_page(self, app_uuid, content_uuid,
                         before=None, after=None, limit=None, offset=None):
        query = {
            'app_uuid': app_uuid,
            'content_uuid': content_uuid
        }
        for k, v in zip(('before', 'after', 'limit', 'offset'),
                        (before, after, limit, offset)):
            if v is not None:
                query[k] = v

        data = self.get('', params=query)
        return CommentPage(self, data)

    def create_comment(self, data):
        try:
            new_data = self.post('', data=data)
        except CommentServiceException as e:
            if e.error_code == 'USER_BANNED':
                raise UserBanned(e.response)
            elif e.error_code == 'STREAM_NOT_OPEN':
                raise CommentStreamNotOpen(e.response)
            raise e

        return Comment(self, new_data)

    def create_flag(self, data):
        resp = self._request_no_parse('post', '/flags/', data=json.dumps(data))
        return resp.status_code == 201

    def delete_flag(self, comment_uuid, user_uuid):
        try:
            self.delete('/flags/%s/%s/' % (comment_uuid, user_uuid))
            return True

        except CommentServiceException as e:
            if e.response.status_code == 404:
                return False
            raise e


class Comment(BaseClientObject):

    def __init__(self, client, data):
        super(Comment, self).__init__(client, data)
        self.coerce_fields()

    def coerce_fields(self):
        self.set('submit_datetime', parse_dt(self.get('submit_datetime')))
        self.set('flag_count', int(self.get('flag_count')))
        self.set('is_removed', self.get('is_removed') in ('true', 'True'))

    def set(self, field, value):
        if field == 'uuid':
            raise ValueError('uuid cannot be set')
        self.data[field] = value

    def get(self, field):
        return self.data[field]

    def flag(self, user_uuid):
        flag_data = {
            'app_uuid': self.get('app_uuid'),
            'comment_uuid': self.get('uuid'),
            'user_uuid': user_uuid,
            'submit_datetime': datetime.now(pytz.utc).isoformat()
        }
        is_new = self.client.create_flag(flag_data)
        if is_new:
            self.set('flag_count', self.get('flag_count') + 1)

    def unflag(self, user_uuid):
        was_deleted = self.client.delete_flag(self.get('uuid'), user_uuid)
        if was_deleted:
            self.set('flag_count', self.get('flag_count') - 1)


class CommentPage(object):

    def __init__(self, client, data):
        self.client = client
        self.data = data

    @property
    def total(self):
        return self.data['total']

    @property
    def start(self):
        return self.data['start']

    @property
    def end(self):
        return self.data['end']

    @property
    def metadata(self):
        return self.data['metadata']

    @property
    def state(self):
        return self.metadata.get('state')

    def __len__(self):
        return self.data['count']

    def __iter__(self):
        for comment_data in self.data['objects']:
            yield Comment(self.client, comment_data)

    def has_next(self):
        return self.total != 0 and self.end < self.total

    def has_previous(self):
        return self.total != 0 and self.start > 1

    def get_next_args(self, **defaults):
        if not self.has_next():
            return None

        args = defaults.copy()
        last_obj = self.data['objects'][-1]
        args.update({
            'before': last_obj.get('uuid'),
            'app_uuid': last_obj.get('app_uuid'),
            'content_uuid': last_obj.get('content_uuid')})
        return args

    def get_previous_args(self, **defaults):
        if not self.has_previous():
            return None

        args = defaults.copy()
        first_obj = self.data['objects'][0]
        args.update({
            'after': first_obj.get('uuid'),
            'app_uuid': first_obj.get('app_uuid'),
            'content_uuid': first_obj.get('content_uuid')})
        return args


class LazyCommentPage(CommentPage):

    def __init__(self, client, **page_args):
        self.client = client
        self._data = None
        self.page_args = page_args

    @property
    def data(self):
        if self._data is None:
            page = self.client.get_comment_page(**self.page_args)
            self._data = page.data
        return self._data
