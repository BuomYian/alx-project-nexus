"""
Admin configuration for accounts app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom user admin"""
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Additional Info', {
            'fields': (
                'phone_number', 'date_of_birth', 'address',
                'city', 'country', 'zip_code', 'profile_picture',
                'is_verified', 'is_email_verified'
            )
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_verified', 'created_at')
    list_filter = ('is_verified', 'is_email_verified', 'created_at')
    search_fields = ('email', 'username', 'first_name', 'last_name')
