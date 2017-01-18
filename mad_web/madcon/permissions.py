from rest_framework import permissions


class IsRegistrant(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object view it.
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner of the object.
        return obj.user == request.user
