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
    
    discount = serializers.SerializerMethodField()
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = Dish
        fields = [
            'id', 'menu', 'dish_category', 'name', 'description',
            'price', 'photo_url', 'created_at', 'updated_at',
            'discount', 'final_price',
        ]
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_discount(self, obj):

        promo = Promotion.objects.filter(dish=obj).first()
        if promo:
            return promo.discount  
        return None

    def get_final_price(self, obj):
        promo = Promotion.objects.filter(dish=obj).first()
        if promo:
            discount_val = float(promo.discount)
            old_price = float(obj.price)
            new_price = old_price * (100 - discount_val) / 100

            return f"{new_price:.2f}"
        return f"{obj.price}"

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