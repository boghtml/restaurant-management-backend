# apps/bookings/views.py
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction

from .models import Booking
from .serializers import BookingSerializer
from apps.restaurants.models import RestaurantTable

class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        user = self.request.user
        if getattr(user, 'role', None) == 'admin':
            return Booking.objects.all()
        else:
            return Booking.objects.filter(user=user)

    def perform_create(self, serializer):

        serializer.save(user=self.request.user, status='Pending')

    @transaction.atomic
    def update(self, request, *args, **kwargs):

        booking = self.get_object()

        if getattr(request.user, 'role', None) != 'admin':
            return Response({"detail": "Only admin can update booking status."},
                            status=status.HTTP_403_FORBIDDEN)

        partial = kwargs.pop('partial', False)
        serializer = self.get_serializer(booking, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        updated_booking = serializer.instance
        if updated_booking.status == 'Confirmed':
            updated_booking.restaurant_table.status = 'Reserved'
            updated_booking.restaurant_table.save()
        elif updated_booking.status == 'Cancelled':

            updated_booking.restaurant_table.status = 'Available'
            updated_booking.restaurant_table.save()

        return Response(serializer.data)

    def partial_update(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):


        if getattr(request.user, 'role', None) != 'admin':
            return Response({"detail": "Only admin can delete bookings."},
                            status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)
