__author__ = 'cltanuki'
from . import serializers, models
from erp.directory import models
from rest_framework import generics


class UserViewSet(generics.ListAPIView):
    model = models.CorpUser
    serializer_class = serializers.UserSerializer


class GroupViewSet(generics.ListAPIView):
    model = models.CorpUnit
    serializer_class = serializers.UnitSerializer
    lookup_field = "title"


class ObjViewSet(generics.ListAPIView):
    model = models.CorpObject
    serializer_class = serializers.ObjSerializer
    lookup_field = "title"


class UserView(generics.RetrieveAPIView):
    model = models.CorpUser
    serializer_class = serializers.UserSerializer


class GroupView(generics.RetrieveAPIView):
    model = models.CorpUnit
    serializer_class = serializers.UnitSerializer


class ObjView(generics.RetrieveAPIView):
    model = models.CorpObject
    serializer_class = serializers.ObjSerializer