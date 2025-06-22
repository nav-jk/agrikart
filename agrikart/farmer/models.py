from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings

class Farmer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name

class Produce(models.Model):
    CATEGORY_CHOICES = [
        ('Fruits', 'Fruits'),
        ('Vegetables', 'Vegetables'),
        ('Grains', 'Grains'),
        ('Dairy', 'Dairy'),
        ('Others', 'Others'),
    ]

    farmer = models.ForeignKey(Farmer, related_name='produce', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Others')

    is_active = models.BooleanField(default=True)  # ✅ New field for availability

    def __str__(self):
        return f"{self.name} ({self.quantity}) - ₹{self.price}"