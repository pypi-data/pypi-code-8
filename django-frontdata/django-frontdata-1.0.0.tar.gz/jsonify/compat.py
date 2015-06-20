# encoding: utf-8

from json import dumps

try:
    from rest_framework.utils.encoders import JSONEncoder
except ImportError:
    from django.core.serializers.json import DjangoJSONEncoder as JSONEncoder


def serialize_data(data):
    return dumps(data, cls=JSONEncoder)
