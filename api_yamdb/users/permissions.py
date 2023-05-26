from rest_framework import permissions


class Moder(permissions.BasePermission):
    """
    Return true for moders.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
               request.user.is_admin
               or request.user.is_superuser
               or request.user.is_moder)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
               request.user.is_admin
               or request.user.is_superuser
               or request.user.is_moder)


class Admin(permissions.BasePermission):
    """
    Return True for admins.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
                request.user.is_admin or request.user.is_superuser)


class Owner(permissions.BasePermission):
    """
    Let owner change its own content.
    """
    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin
                or request.user.is_superuser
                )


class ReadOnlyOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or (request.user.is_authenticated and (request.user.is_admin or request.user.is_superuser))
