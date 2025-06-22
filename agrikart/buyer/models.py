from django.db import models
from django.conf import settings
from farmer.models import Produce
from django.utils import timezone

class Buyer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - Buyer"

class CartItem(models.Model):
    buyer = models.ForeignKey(Buyer, related_name='cart', on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.produce.name} x {self.quantity}"

    class Meta:
        unique_together = ('buyer', 'produce')

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('PICKED_UP', 'Picked Up'),
        ('IN_TRANSIT', 'In Transit'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    buyer = models.ForeignKey(Buyer, related_name='orders', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(default=timezone.now)

    # 🆕 Add these fields:
    buyer_lat = models.FloatField(null=True, blank=True)
    buyer_lon = models.FloatField(null=True, blank=True)
    farmer_lat = models.FloatField(null=True, blank=True)
    farmer_lon = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Order {self.id} - {self.status}"
