# apps/menus/serializers.py
from rest_framework import serializers
from .models import Menu

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['id', 'restaurant', 'name', 'photo_url', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')


from .models import Dish, DishCategory, Promotion

class DishSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dish
        fields = [
            'id', 'menu', 'dish_category', 'name', 'description',
            'price', 'photo_url', 'created_at', 'updated_at'
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

class DishCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DishCategory
        fields = ['id', 'name', 'description', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'dish', 'title', 'description', 'discount', 'created_at', 'updated_at']
        read_only_fields = ('id', 'created_at', 'updated_at')