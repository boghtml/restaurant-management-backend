# apps/bookings/serializers.py
from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Booking
        fields = [
            'id', 'restaurant_table', 'user', 'status',
            'booking_time', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'status',
            'created_at', 'updated_at'
        ]
