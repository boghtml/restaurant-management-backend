
from rest_framework.permissions import IsAuthenticated
from .serializers import RestaurantSerializer, RestaurantTableSerializer
from .models import Restaurant, RestaurantTable
from .permissions import IsAdminOrReadOnly

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction

class IsAdminRole(IsAuthenticated):
    """
    Дозволяє доступ лише для користувачів зі спеціальним role = 'admin'.
    """
    def has_permission(self, request, view):
        is_auth = super().has_permission(request, view)
        if not is_auth:
            return False
        return getattr(request.user, 'role', None) == 'admin'

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    permission_classes = [IsAdminOrReadOnly]


class RestaurantTableViewSet(viewsets.ModelViewSet):
    queryset = RestaurantTable.objects.all()
    serializer_class = RestaurantTableSerializer
    permission_classes = [IsAdminOrReadOnly]  

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path='occupy')
    def occupy_table(self, request, pk=None):
        """
        POST /api/restaurants/tables/{id}/occupy/
        (лише admin) - змінює table.status -> 'Occupied'
        """
        user = request.user
        if getattr(user, 'role', None) != 'admin':
            return Response({"detail": "Only admin can occupy a table."},
                            status=status.HTTP_403_FORBIDDEN)

        table = self.get_object()
        table.status = 'Occupied'
        table.save()

        serializer = self.get_serializer(table)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path='free')
    def free_table(self, request, pk=None):
        """
        POST /api/restaurants/tables/{id}/free/
        (лише admin) - змінює table.status -> 'Available'
        """
        user = request.user
        if getattr(user, 'role', None) != 'admin':
            return Response({"detail": "Only admin can free a table."},
                            status=status.HTTP_403_FORBIDDEN)

        table = self.get_object()
        table.status = 'Available'
        table.save()

        serializer = self.get_serializer(table)
        return Response(serializer.data, status=status.HTTP_200_OK)