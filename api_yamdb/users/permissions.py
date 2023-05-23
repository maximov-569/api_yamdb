from rest_framework import permissions


class Admin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'admin':
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return False


class Owner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user == obj:
            return True
        return False
