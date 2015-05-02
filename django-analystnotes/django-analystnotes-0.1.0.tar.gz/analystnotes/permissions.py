"""
Permissions for django-analystnotes. While we could have used the builtin django object permissions,
it is a more consistent experience to just do it inside the application. This has 2 advantages:
1) No third party dependencies for auth/authorization.
2) Mis-configurations won't result in exposing users private data.
"""
from rest_framework import permissions


class ObjectOwnerPermission(permissions.BasePermission):
    """
    Requests on everything but post requires object permissions.
    """

    def has_object_permission(self, request, view, obj):
        # If no owner permission granted
        if not hasattr(obj, 'owner'):
            return False
        # If this is owned by the user, the user has permission to modify object
        if request.user == obj.owner:
            return True
        return False


class ProjectOwnerPermission(permissions.BasePermission):
    """
    Requests on everything but post requires object permissions.
    Technically this shouldn't run, since filtering should take care of most use cases.
    """

    def has_object_permission(self, request, view, obj):
        # If no project defined for object
        # in theory this shouldn't happen... but if it does, we should bail out
        if not hasattr(obj, 'project'):
            return False
        # Check to see that the parent projects owner is the logged in user.
        # Later on we can do group checks as well using this function if there is need.
        if obj.project.owner == request.user:
            return True
        return False
