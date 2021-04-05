from rest_framework import permissions


class IsOrderOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            return obj.profile == request.user.profile
