from django.db import models
from apps.restaurants.models import RestaurantTable
from django.conf import settings  

class Booking(models.Model):
    BOOKING_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    )

    restaurant_table = models.ForeignKey(
        RestaurantTable, 
        on_delete=models.CASCADE, 
        related_name='bookings'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bookings'
    )
    status = models.CharField(max_length=20, choices=BOOKING_STATUS_CHOICES, default='Pending')
    booking_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Booking #{self.id} by {self.user.username}'
