from rest_framework import serializers
from datetime import timedelta
from django.utils import timezone

from .models import Restaurant, RestaurantTable
from apps.bookings.models import Booking

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'email', 'photo_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RestaurantTableSerializer(serializers.ModelSerializer):
    
    status = serializers.SerializerMethodField()

    class Meta:
        model = RestaurantTable
        fields = [
            'id', 'restaurant', 'table_number', 'seats',
            
            'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_status(self, obj):
        """
        Якщо у діапазоні [now - 15хв, now + 30хв] існує бронювання
        (не Cancelled), то повертаємо 'Reserved',
        інакше повертаємо те, що зберігається у obj.status (Available, Occupied...).
        """
        now = timezone.now()
        start_check = now - timedelta(minutes=15)
        end_check = now + timedelta(minutes=30)

        conflict_exists = Booking.objects.filter(
            restaurant_table=obj,
            booking_time__range=(start_check, end_check)
        ).exclude(status='Cancelled').exists()

        if conflict_exists:
            return 'Reserved'

        return obj.status
