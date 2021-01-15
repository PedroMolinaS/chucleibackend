from django.contrib.auth.models import Group
from rest_framework import permissions


def _is_in_group(user, group_name):
    try:
        return Group.objects.get(name=group_name).user_set.filter(id=user.id).exists()
    except Group.DoesNotExist:
        return None


def _has_group_permission(user, required_groups):
    return any([_is_in_group(user, group_name) for group_name in required_groups])


class IsLoggedInUserOrAdmin(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['admin']

    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        if self.required_groups is None:
            return False
        return obj == request.user or has_group_permission


class IsAdminUser(permissions.BasePermission):
    # group_name for super admin
    required_groups = ['admin']

    # has_permission () es para el permiso a nivel de usuario
    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission

    # has_object_permission() es permiso a nivel de objeto
    def has_object_permission(self, request, view, obj):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission


class IsAdminOrAnonymousUser(permissions.BasePermission):
    required_groups = ['anonymus']

    def has_permission(self, request, view):
        has_group_permission = _has_group_permission(request.user, self.required_groups)
        return request.user and has_group_permission
