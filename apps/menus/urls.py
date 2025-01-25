# apps/menus/urls.py
from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import MenuViewSet, DishViewSet, DishCategoryViewSet, PromotionViewSet

router = DefaultRouter()
router.register(r'menus', MenuViewSet, basename='menu')
router.register(r'dishes', DishViewSet, basename='dish')
router.register(r'dishcategories', DishCategoryViewSet, basename='dishcategory')
router.register(r'promotions', PromotionViewSet, basename='promotion')

urlpatterns = [
    path('', include(router.urls)),
]
