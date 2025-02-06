# apps/bookings/views.py
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import timedelta

from .models import Booking
from .serializers import BookingSerializer
from apps.restaurants.models import RestaurantTable
from apps.restaurants.permissions import IsAdminOrReadOnly


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        - Якщо користувач - admin: повертаємо всі бронювання.
        - Інакше: лише власні (user == request.user).
        """
        user = self.request.user
        if getattr(user, 'role', None) == 'admin':
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    def perform_create(self, serializer):
        """
        1) Присвоюємо user = request.user, status = 'Pending'
        2) Перевіряємо, чи немає конфлікту за часом (±15хв, +30хв)
        """
        # Перевіримо на конфлікт:
        data = serializer.validated_data
        restaurant_table = data['restaurant_table']
        new_booking_time = data['booking_time']

        # Часовий діапазон: [booking_time - 15 хв, booking_time + 30 хв]
        start_check = new_booking_time - timedelta(minutes=15)
        end_check = new_booking_time + timedelta(minutes=30)

        # Перевіримо в БД, чи вже існує бронювання на цей столик,
        # час якого потрапляє у наш проміжок (перетинається)
        conflict_exists = Booking.objects.filter(
            restaurant_table=restaurant_table,
            booking_time__range=(start_check, end_check)
        ).exclude(status='Cancelled').exists()

        if conflict_exists:
            raise ValidationError("Столик уже заброньовано на даний час (з урахуванням 15хв до та 30хв після).")

        # Якщо конфлікту немає:
        serializer.save(
            user=self.request.user,
            status='Pending'
        )

    def update(self, request, *args, **kwargs):
        """
        Можемо взагалі прибрати логіку оновлення статусу тут
        або залишити для update (наприклад, зміна часу, столика),
        але без призначення table.status.
        """
        # Перевіримо чи admin
        if getattr(request.user, 'role', None) != 'admin':
            return Response(
                {"detail": "Only admin can update booking."},
                status=status.HTTP_403_FORBIDDEN
            )

        return super().update(request, *args, **kwargs)

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path='confirm')
    def confirm_booking(self, request, pk=None):
        """
        POST /api/bookings/bookings/{id}/confirm/
        (лише admin) - змінює status -> 'Confirmed'
        """
        if getattr(request.user, 'role', None) != 'admin':
            return Response({"detail": "Only admin can confirm booking."},
                            status=status.HTTP_403_FORBIDDEN)

        booking = self.get_object()
        booking.status = 'Confirmed'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    @transaction.atomic
    @action(detail=True, methods=['post'], url_path='occupy')
    def occupy_booking(self, request, pk=None):
        """
        POST /api/bookings/bookings/{id}/occupy/
        (лише admin) - змінює status -> 'Occupied'
        """
        if getattr(request.user, 'role', None) != 'admin':
            return Response({"detail": "Only admin can mark booking as occupied."},
                            status=status.HTTP_403_FORBIDDEN)

        booking = self.get_object()
        booking.status = 'Occupied'
        booking.save()
        serializer = self.get_serializer(booking)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Видаляти бронювання може лише admin
        """
        if getattr(request.user, 'role', None) != 'admin':
            return Response({"detail": "Only admin can delete bookings."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
