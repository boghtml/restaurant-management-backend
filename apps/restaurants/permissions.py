# apps/restaurants/permissions.py
from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Дозволяє GET (читання) всім,
    але створення/редагування/видалення – лише користувачу з role='admin'.
    """

    def has_permission(self, request, view):
    
        if request.method in permissions.SAFE_METHODS:
            return True
    
        return (
            request.user.is_authenticated
            and getattr(request.user, 'role', None) == 'admin'
        )
