import binascii
import json
import logging
import zlib
from base64 import urlsafe_b64decode
from datetime import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers


logger = logging.getLogger(__name__)


##########
# Form Fields
##########


class IPAddressField(forms.GenericIPAddressField):
    """IPAddressField which strips port

    Splits the port from the value before interpreting it as an ip address.
    For ipv6 this takes the non-standard form `ip:port`, if port is specified
    empty groups must be explicitly written. (e.g.
    `2001:db8:85a3::::370:7334:port` not `2001:db8:85a3::370:7334:port`)
    """
    def to_python(self, value):
        try:
            value = value.strip()
        except AttributeError:
            raise ValidationError('Value must be a string', code='invalid')

        addr, port = value, None
        if '.' in value and ':' in value:
            # ipv4 or ipv6-packed ipv4
            port_start = value.rfind(':', value.rfind('.'))
            if port_start != -1:
                addr, port = value[:port_start], value[port_start + 1:]
        elif value.count(':') == 8:
            # ipv6 with port
            addr, port = value.rsplit(':', 1)

        addr = super(IPAddressField, self).to_python(addr)
        if port:
            try:
                port = int(port)
            except ValueError:
                raise ValidationError('Port must be an integer')
        else:
            port = None

        return addr, port

    def validate(self, value):
        addr, port = value
        super(IPAddressField, self).validate(addr)

    def run_validators(self, value):
        addr, port = value
        super(IPAddressField, self).run_validators(addr)


class GzipJsonField(forms.Field):
    """Field which expects urlsafe-base64 encoded gzipped data"""

    def to_python(self, value):
        # Value must be `Unicode` type on PY2
        try:
            value = value.encode('utf-8')
        except ValueError:
            raise ValidationError('Couldnt UTF-8 encode value', code='invalid')

        try:
            value = urlsafe_b64decode(value)
        except (TypeError, binascii.Error):
            raise ValidationError('Couldnt base64 decode value', code='invalid')

        try:
            value = zlib.decompress(value)
        except zlib.error:
            raise ValidationError('Couldnt zlib decompress value', code='invalid')

        try:
            value = value.decode('utf-8')
        except ValueError:
            raise ValidationError('Couldnt UTF-8 decode the decompressed value', code='invalid')

        try:
            value = json.loads(value)
        except (TypeError, ValueError):
            raise ValidationError('Couldnt parse value as JSON', code='invalid')

        return super(GzipJsonField, self).to_python(value)


##########
# Serializer Fields
##########


class TimestampField(serializers.Field):
    """Convert POSIX timestamps to/from TZ-aware datetime objects"""
    default_error_messages = {
        'invalid': 'Must be a TZ-aware datetime object',
    }

    def to_representation(self, obj):
        """Convert a TZ-aware datetime to its POSIX timestamp"""
        if timezone.is_naive(obj):
            self.fail('invalid')
        return (obj - datetime(1970, 1, 1, tzinfo=timezone.utc)).total_seconds()

    def to_internal_value(self, data):
        """Convert a POSIX timestamp to a TZ-aware datetime"""
        return datetime.utcfromtimestamp(data).replace(tzinfo=timezone.utc)
