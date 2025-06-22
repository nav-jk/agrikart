from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from buyer.models import Order

class LogisticsPartner(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.name


class CourierAssignment(models.Model):
    courier = models.ForeignKey(LogisticsPartner, on_delete=models.CASCADE)
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    distance_km = models.FloatField()
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.courier.name} -> Order #{self.order.id}"