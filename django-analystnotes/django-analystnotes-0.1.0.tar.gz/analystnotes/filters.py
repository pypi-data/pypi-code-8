from rest_framework import filters
from django.db.models import Q


class ObjectOwnerFieldPermissionsFilter(filters.BaseFilterBackend):
    """
    A filter backend that limits results to those where the requesting user
    has read object level permissions.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class ProjectOwnerFieldPermissionsFilter(filters.BaseFilterBackend):
    """
    A filter backend that limits results to those where the requesting user
    has read object level permissions.
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.filter(project__owner=request.user)


class OrderByNameFilter(filters.BaseFilterBackend):
    """
    Basic Filter to order records by name
    """

    def filter_queryset(self, request, queryset, view):
        return queryset.order_by('name')
