from rest_framework import serializers
from .models import *

class SiteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Site

class SignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Signature
        fields = ('site','owner',)


class SignatureResponseSerializer(serializers.ModelSerializer):
    site = SiteSerializer()
    class Meta:
        model = Signature
        fields = ('site','owner','key')