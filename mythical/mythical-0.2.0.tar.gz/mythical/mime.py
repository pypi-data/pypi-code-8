import datetime
import json
import urllib

from . import pilo


urlencoded_type = 'application/x-www-form-urlencoded'

json_type = 'application/json'

accept_types = 'application/json'



def encode_json_default(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return obj


def encode_json(data):
    return json.dumps(
        data,
        indent=4,
        sort_keys=True,
        default=encode_json_default,
    )


def encode_qs(data):
    return urllib.urlencode(
        dict((k, v) for k, v in data.iteritems() if v is not None)
    )


def encoder_for(content_type):
    if content_type == json_type:
        return encode_json
    if content_type == urlencoded_type:
        return encode_qs
    raise LookupError('No encoder for content-type "{}"'.format(content_type))


json_source = pilo.source.JsonSource


def source_for(content_type):
    if content_type == json_type:
        return json_source
    raise LookupError('No source for content-type "{}"'.format(content_type))
