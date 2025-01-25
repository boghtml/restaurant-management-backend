from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import RestaurantSerializer
from .models import Restaurant
from .permissions import IsAdminOrReadOnly


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
