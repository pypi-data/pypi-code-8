__author__ = 'cltanuki'
from . import models
from erp.enterprise.serializers import UnitSerializer
from rest_framework import serializers


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Position
        fields = ('id', 'unit', 'title', 'since', 'until')


class PositionFullSerializer(PositionSerializer, serializers.ModelSerializer):

    unit = UnitSerializer()


class EMailSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.EMail
        fields = ('id', 'cat', 'body')


class PhoneSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Phone
        fields = ('id', 'cat', 'country_code', 'area_code', 'number')

#

class PersonSerializer(serializers.ModelSerializer):

    emails = EMailSerializer(many=True, read_only=True)
    phones = PhoneSerializer(many=True, read_only=True)
    positions = PositionSerializer(many=True, read_only=True)

    class Meta:
        model = models.Person
        #fields = ('id', 'first_name', 'mid_name', 'last_name', 'emails', 'positions', 'phones') #
        fields = ('user', 'first_name', 'last_name', 'mid_name', 'date_of_birth', 'sex',
                  'avatar', 'emails', 'positions', 'phones')


# class AddressSerializer(serializers.HyperlinkedModelSerializer):
#
#     class Meta:
#         model = models.Address
#         fields = ('person', 'title', 'unit')
