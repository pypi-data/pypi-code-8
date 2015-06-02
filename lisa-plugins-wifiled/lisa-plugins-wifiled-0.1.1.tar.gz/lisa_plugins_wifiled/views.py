from models import Configuration
from rest_framework import viewsets
from serializers import ConfigurationSerializer


class ConfigurationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to add/edit/delete shopping lists.
    """
    queryset = Configuration.objects.all()
    serializer_class = ConfigurationSerializer
