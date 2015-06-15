import collections
import datetime
import json
import logging
import urllib
import uuid

from mythicals import form, Form


logger = logging.getLogger(__name__)


MIME = collections.namedtuple(
    'MIME', ['type', 'encoder', 'encode', 'decode', 'source', 'extension']
)

class Selection(list):

    @property
    def types(self):
        return map(lambda x: x.type, self)

    def match_type(self, type):
        for mime in self:
            if mime.type == type:
                return mime

    match = match_type

    def match_extension(self, ext):
        if ext.startswith('.'):
            ext = ext[1:]
        for mime in self:
            if mime.extension == ext:
                return mime

# json

class JSONEncoder(json.JSONEncoder):

    def _datetime(self, o):
        return o.isoformat()

    def _date(self, o):
        return '{:04d}-{:02d}-{:02d}'.format(o.year, o.month, o.day)

    def _time(self, o):
        return o.strftime('%H:%M:%S')

    def _uuid(self, o):
        return str(o)

    # json.JSONEncoder

    def __init__(self, errors='strict', *args, **kwargs):
        self.errors = errors
        super(JSONEncoder, self).__init__(*args, **kwargs)

    def default(self, o):
        if isinstance(o, datetime.datetime):
            return self._datetime(o)
        if isinstance(o, datetime.date):
            return self._date(o)
        if isinstance(o, datetime.time):
            return self._time(o)
        if isinstance(o, uuid.UUID):
            return self._uuid(o)
        if self.errors == 'ignore':
            return
        if self.errors == 'warn':
            logger.warning(repr(o) + ' is not JSON serializable')
            return
        return super(JSONEncoder, self).default(o)

    def iterencode(self, o, _one_shot=False):
        if isinstance(o, Form):
            o = dict(o)
        return super(JSONEncoder, self).iterencode(o, _one_shot=_one_shot)


json = MIME(
    type='application/json',
    encoder=JSONEncoder,
    encode=JSONEncoder(indent=4, sort_keys=True).encode,
    decode=json.load,
    source=form.JSONSource,
    extension='json'
)

# url

class URLEncoder(object):

    def __init__(self, exclude_none=True, doseq=1, errors='strict'):
        super(URLEncoder, self).__init__()
        self.exclude_none = exclude_none
        self.doseq = doseq
        self.errors = errors

    def encode(self, o):

        query = []

        def _encode_value(key, value):
            if value is None and self.exclude_none:
                return
            if isinstance(value, (list, tuple)):
                for v in value:
                    _encode_value(key, v)
                return
            if not isinstance(value, basestring):
                v = self.default(value)
            if value is None and self.exclude_none:
                return
            query.append((key, value))

        for k, v in o.iteritems():
            _encode_value(k, v)

        return urllib.urlencode(query, self.doseq)

    def default(self, o):
        if isinstance(o, (int, long)):
            return str(o)
        if isinstance(o, bool):
            return 'true' if o else 'false'
        if isinstance(o, datetime.datetime):
            return self._datetime(o)
        if self.errors == 'strict':
            raise TypeError(repr(o) + ' is not URL serializable')
        if self.errors == 'warn':
            logger.warning(repr(o) + ' is not URL serializable')

    def _datetime(self, value):
        return value.isoformat()

    def _date(self, o):
        return o.strftime('%Y-%m-%d')

    def _time(self, o):
        return o.strftime('%H:%M:%S')


url = MIME(
    type='application/x-www-form-urlencoded',
    encoder=URLEncoder,
    encode=URLEncoder(exclude_none=True, doseq=1).encode,
    decode=None,
    source=None,
    extension='url'
)
