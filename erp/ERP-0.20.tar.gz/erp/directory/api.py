__author__ = 'cltanuki'
from rest_framework import mixins, generics, viewsets, response
from . import serializers, models


from django.shortcuts import get_object_or_404




class PersonBase():

    def get_queryset(self):
        person_id = self.kwargs.get('person_pk')
        person = get_object_or_404(models.Person, pk=person_id)
        queryset = self.model.objects.filter(person=person)
        return queryset

    def perform_create(self, serializer):
        person_id = self.kwargs.get('person_pk')
        person = get_object_or_404(models.Person, pk=person_id)
        serializer.save(person=person)


class PhonesViewSet(PersonBase, viewsets.ModelViewSet):

    serializer_class = serializers.PhoneSerializer
    model = models.Phone


class PositionsViewSet(PersonBase, viewsets.ModelViewSet):

    model = models.Position

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.PositionFullSerializer
        return serializers.PositionSerializer


class EMailsViewSet(PersonBase, viewsets.ModelViewSet):

    serializer_class = serializers.EMailSerializer
    model = models.EMail


class PersonsViewSet(viewsets.ModelViewSet):

    serializer_class = serializers.PersonSerializer
    queryset = models.Person.objects.all()