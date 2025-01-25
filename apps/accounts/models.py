from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):

    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    ROLE_CHOICES = (
        ('client', 'Client'),
        ('admin', 'Admin'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')

    def __str__(self):
        return self.username
