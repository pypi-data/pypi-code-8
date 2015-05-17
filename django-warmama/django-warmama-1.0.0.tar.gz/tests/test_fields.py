import json
import zlib
from base64 import urlsafe_b64encode
from datetime import datetime
from django import forms
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import ValidationError as DrfValidationError
from tests import TestCase
from warmama import fields


class IPAddressFieldTest(TestCase):
    class SampleForm(forms.Form):
        ipaddr = fields.IPAddressField(unpack_ipv4=True)

    def test_ipv6(self):
        """Test strip ipv6 port"""
        # TODO: this is a non-standard way to write ipv6+port, but its what
        # qfusion does. It should be [ipv6]:port
        form = self.SampleForm({
            'ipaddr': '2001:0db8:85a3:0000:0000:8a2e:0370:7334:44400'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['ipaddr'], ('2001:db8:85a3::8a2e:370:7334', 44400))

    def test_ipv4(self):
        """Test strip ipv4 port"""
        form = self.SampleForm({
            'ipaddr': '192.102.2.1:44400'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['ipaddr'], ('192.102.2.1', 44400))

    def test_packed_ipv4(self):
        """It strip packed ipv4 port"""
        form = self.SampleForm({
            'ipaddr': '::ffff:192.102.2.1:44400'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['ipaddr'], ('192.102.2.1', 44400))

    def test_ipv6_noport(self):
        """Test ipv6 without port"""
        form = self.SampleForm({
            'ipaddr': '2001:0db8:85a3:0000:0000:8a2e:0370:7334'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['ipaddr'], ('2001:db8:85a3::8a2e:370:7334', None))

    def test_ipv4_noport(self):
        """Test ipv4 without port"""
        form = self.SampleForm({
            'ipaddr': '192.102.2.1'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['ipaddr'], ('192.102.2.1', None))

    def test_packed_ipv4_noport(self):
        """It packed ipv4 without port"""
        form = self.SampleForm({
            'ipaddr': '::ffff:192.102.2.1'
        })

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['ipaddr'], ('192.102.2.1', None))

    def test_invalid_input(self):
        """It should invalidate bad inputs"""
        form = self.SampleForm({'ipaddr': 3})

        self.assertFalse(form.is_valid())


class GzipJsonFieldTest(TestCase):
    class SampleForm(forms.Form):
        data = fields.GzipJsonField()

    def test_valid_field(self):
        data = {'a': 1, 'b': [True, "2", None]}
        packed = json.dumps(data).encode('utf-8')
        packed = zlib.compress(packed)
        packed = urlsafe_b64encode(packed).decode('ascii')
        form = self.SampleForm({'data': packed})

        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data['data'], data)


class TimestampFieldTest(TestCase):
    class SampleSerializer(serializers.Serializer):
        """Sample serializer to test TimestampField"""
        datetime = fields.TimestampField()

    class Timestamp(object):
        """Sample object that can be serialized with SampleSerializer"""
        def __init__(self, dt):
            self.datetime = dt

    def test_deserialize(self):
        """It should return correct values for sample times"""
        ts, dt = 0, datetime(1970, 1, 1, tzinfo=timezone.utc)
        serializer = self.SampleSerializer(data={'datetime': ts})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['datetime'], dt)

        ts, dt = 1420070400, datetime(2015, 1, 1, tzinfo=timezone.utc)
        serializer = self.SampleSerializer(data={'datetime': ts})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['datetime'], dt)

    def test_serialize(self):
        ts, obj = 0, self.Timestamp(datetime(1970, 1, 1, tzinfo=timezone.utc))
        serializer = self.SampleSerializer(instance=obj)
        self.assertEqual(serializer.data['datetime'], ts)

        ts, obj = 1420070400, self.Timestamp(datetime(2015, 1, 1, tzinfo=timezone.utc))
        serializer = self.SampleSerializer(instance=obj)
        self.assertEqual(serializer.data['datetime'], ts)

    def test_naive(self):
        obj = self.Timestamp(datetime(1970, 1, 1))
        serializer = self.SampleSerializer(instance=obj)

        with self.assertRaises(DrfValidationError):
            serializer.data
