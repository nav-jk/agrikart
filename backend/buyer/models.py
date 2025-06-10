from django.db import models
from farmer.models import Produce

class Buyer(models.Model):
    phone_number = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField()

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

class CartItem(models.Model):
    buyer = models.ForeignKey(Buyer, related_name='cart', on_delete=models.CASCADE)
    produce = models.ForeignKey(Produce, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Order(models.Model):
    buyer = models.ForeignKey(Buyer, related_name='orders', on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    created_at = models.DateTimeField(auto_now_add=True)
