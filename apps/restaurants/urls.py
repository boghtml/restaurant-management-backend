from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, RestaurantTableViewSet

router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet, basename='restaurant')
router.register(r'tables', RestaurantTableViewSet, basename='restaurant-table')

urlpatterns = [
    path('', include(router.urls)),
]
