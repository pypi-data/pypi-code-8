__author__ = 'cltanuki'
from rest_framework import serializers

from .models import CorpUser
from erp.directory.models import CorpUnit, CorpObject

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CorpUser
        fields = ('username',)


class UnitSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CorpUnit
        fields = ('id', 'title', 'parent')


class UnitListSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CorpUnit
        fields = ('id', 'title', 'parent')


class ObjSerializer(serializers.HyperlinkedModelSerializer):
    parent = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = CorpObject
        fields = ('id', 'title', 'parent')

# TODO: What is it???
#UnitSerializer.fields['parent'] = UnitSerializer()
#ObjSerializer.fields['parent'] = ObjSerializer()