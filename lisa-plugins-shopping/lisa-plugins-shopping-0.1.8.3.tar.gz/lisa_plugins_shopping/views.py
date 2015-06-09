from lisa_plugins_shopping.models import ShoppingList
from rest_framework import viewsets
from serializers import ShoppingListSerializer


class ShoppingListViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to add/edit/delete shopping lists.
    """
    queryset = ShoppingList.objects.all()
    serializer_class = ShoppingListSerializer
