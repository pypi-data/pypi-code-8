from models import ShoppingList
from rest_framework import serializers


class ShoppingListSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ShoppingList
        fields = ('url', 'name', 'list')
