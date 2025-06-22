from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    is_farmer = models.BooleanField(default=False)
    is_buyer = models.BooleanField(default=False)
    is_logistics = models.BooleanField(default=False) 

    REQUIRED_FIELDS = ['phone_number', 'email']  # ✅ Add phone_number here
    
    def __str__(self):
        return self.username
