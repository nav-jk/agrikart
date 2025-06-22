from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        'username', 'email', 'phone_number',
        'is_farmer', 'is_buyer', 'is_logistics',  # ✅ added here
        'is_staff', 'is_superuser'
    )
    list_filter = (
        'is_farmer', 'is_buyer', 'is_logistics',  # ✅ added here
        'is_staff', 'is_superuser'
    )

    fieldsets = UserAdmin.fieldsets + (
        (None, {
            'fields': ('phone_number', 'is_farmer', 'is_buyer', 'is_logistics')  # ✅ added here
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {
            'fields': ('phone_number', 'is_farmer', 'is_buyer', 'is_logistics'),  # ✅ added here
        }),
    )

    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
