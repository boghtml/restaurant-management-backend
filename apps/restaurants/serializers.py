from rest_framework import serializers
from .models import Restaurant, RestaurantTable

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'email', 'photo_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class RestaurantTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantTable
        fields = ['id', 'restaurant', 'table_number', 'seats', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']