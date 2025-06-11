from django.contrib import admin
from .models import Buyer, CartItem, Order

@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ('user', 'address')
    search_fields = ('user__username', 'user__phone_number', 'user__email')

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'produce', 'quantity')
    list_filter = ('produce',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'buyer', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('buyer__user__username',)
    filter_horizontal = ('items',)
