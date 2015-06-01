from rest_framework import viewsets
from rest_framework.pagination import CursorPagination
from .serializers import ActionSerializer
from .models import Action


class ActionCursorPagination(CursorPagination):
    ordering = 'id'


class ActionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Action.objects.all().select_related().prefetch_related(
        'target', 'actor')
    serializer_class = ActionSerializer
    pagination_class = ActionCursorPagination
    filter_fields = (
        'actor_content_type', 'actor_content_type__model',
        'target_content_type', 'target_content_type__model',
    )
