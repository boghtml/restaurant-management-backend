# apps/accounts/urls.py
from django.urls import path
from .views import UserRegistrationView, CurrentUserView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('me/', CurrentUserView.as_view(), name='current_user'),

]
