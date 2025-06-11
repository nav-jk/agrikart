from django.contrib import admin
from .models import Farmer, Produce

@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'address')
    search_fields = ('user__username', 'user__phone_number', 'name')
    list_filter = ('address',)

@admin.register(Produce)
class ProduceAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'price', 'quantity')
    search_fields = ('name', 'farmer__name', 'farmer__user__username')
    list_filter = ('farmer',)
