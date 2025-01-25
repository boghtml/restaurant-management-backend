# apps/menus/views.py
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Menu, Dish, Promotion, DishCategory
from .serializers import MenuSerializer, DishSerializer, DishCategorySerializer, PromotionSerializer
from apps.restaurants.permissions import IsAdminOrReadOnly 

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    permission_classes = [IsAdminOrReadOnly]

    @action(detail=True, methods=['get'], url_path='full-details')
    def full_details(self, request, pk=None):
        """
        Кастомний ендпоінт для отримання:
         - назви меню,
         - усіх страв з категоріями,
         - з урахуванням діючих знижок (якщо є).
        Приклад URI: GET /api/menus/1/full-details/
        """
        menu = self.get_object() 
        dishes = Dish.objects.filter(menu=menu).select_related('dish_category')

             
        dish_list = []
        for dish in dishes:

            promotions = Promotion.objects.filter(dish=dish)
        
            discount_info = None
            if promotions.exists():
                promo = promotions.first()
                discount_percentage = float(promo.discount)
                new_price = float(dish.price) * (100 - discount_percentage) / 100
                discount_info = {
                    "promotion_title": promo.title,
                    "original_price": float(dish.price),
                    "discount_percentage": discount_percentage,
                    "new_price": new_price
                }

            dish_list.append({
                "dish_id": dish.id,
                "name": dish.name,
                "category": dish.dish_category.name if dish.dish_category else None,
                "price": float(dish.price),
                "discount_info": discount_info
            })

        data = {
            "menu_id": menu.id,
            "menu_name": menu.name,
            "restaurant_id": menu.restaurant_id,
            "dishes": dish_list
        }
        return Response(data)


class DishViewSet(viewsets.ModelViewSet):
    queryset = Dish.objects.all()
    serializer_class = DishSerializer
    permission_classes = [IsAdminOrReadOnly]


class DishCategoryViewSet(viewsets.ModelViewSet):
    queryset = DishCategory.objects.all()
    serializer_class = DishCategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAdminOrReadOnly]
