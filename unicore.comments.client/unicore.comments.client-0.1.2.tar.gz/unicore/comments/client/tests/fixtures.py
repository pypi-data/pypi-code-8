import json
from datetime import datetime
import pytz
from uuid import uuid4


'''
Comment fixtures
'''


comment_data = {
    'uuid': 'd269f09c4672400da4250342d9d7e1e4',
    'user_uuid': '2923280ee1904478bfcf7a46f26f443b',
    'content_uuid': 'f587b74816bb425ab043f1cf30de7abe',
    'app_uuid': 'bbc0035128b34ed48bdacab1799087c5',
    'comment': 'this is a comment',
    'user_name': 'foo',
    'submit_datetime': datetime.now(pytz.utc).isoformat(),
    'content_type': 'page',
    'content_title': 'I Am A Page',
    'content_url': 'http://example.com/page/',
    'locale': 'eng_ZA',
    'flag_count': '0',
    'is_removed': 'False',
    'moderation_state': 'visible',
    'ip_address': '192.168.1.1'
}
comment_json = json.dumps(comment_data)
comment_stream_data = {
    'start': 20,
    'end': 30,
    'total': 100,
    'count': 10,
    'objects': map(
        lambda i: dict(comment_data.items() + [('uuid', uuid4().hex)]),
        range(10)),
    'metadata': {'state': 'open'}
}
comment_stream_json = json.dumps(comment_stream_data)


'''
Flag fixtures
'''


flag_data = {
    'app_uuid': 'bbc0035128b34ed48bdacab1799087c5',
    'comment_uuid': 'd269f09c4672400da4250342d9d7e1e4',
    'user_uuid': 'f0ee8eac105b485287d7633673dc93ef',
    'submit_datetime': datetime.now(pytz.utc).isoformat(),
}
flag_json = json.dumps(flag_data)


'''
Error fixtures
'''


generic_error_data = {
    'status': 'error',
    'error_code': 'ERROR_CODE',
    'error_dict': {},
    'error_message': 'ERROR_MESSAGE',
}
generic_error_json = json.dumps(generic_error_data)
