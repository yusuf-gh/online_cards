from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('manager', 'Users Manager'),
        ('admin', 'Administration')
    )
    
    user_type = models.CharField(
        max_length=14,
        choices=USER_TYPE_CHOICES,
        default='regular'
    )

    def __str__(self):
        return self.username
