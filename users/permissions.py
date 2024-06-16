from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем."""

    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


class IsUser(permissions.BasePermission):
    """Проверяет, является ли пользователь пользователем."""

    def has_object_permission(self, request, view, obj):
        print(request.user)
        print(obj)
        return request.user == obj
