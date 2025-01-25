from rest_framework import serializers
from .models import Restaurant

class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = ['id', 'name', 'address', 'phone', 'email', 'photo_url', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
