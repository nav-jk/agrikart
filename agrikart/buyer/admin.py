from django.contrib import admin
from .models import Buyer, CartItem, Order

admin.site.register(Buyer)
admin.site.register(CartItem)
admin.site.register(Order)
