from models import Configuration
from rest_framework import serializers


class ConfigurationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Configuration
        fields = ('room', 'address', 'port')
