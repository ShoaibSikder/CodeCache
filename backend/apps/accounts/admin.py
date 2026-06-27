"""
Admin configuration for the accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = [
        'username', 'email', 'full_name', 'role',
        'is_active', 'created_at'
    ]
    list_filter = ['role', 'is_active', 'created_at']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-created_at']
    readonly_fields = ['id', 'created_at', 'updated_at', 'last_login']

    fieldsets = [
        (None, {'fields': ['id', 'username', 'email', 'password']}),
        ('Personal Info', {'fields': ['first_name', 'last_name']}),
        ('Permissions', {'fields': ['role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions']}),
        ('Important Dates', {'fields': ['last_login', 'created_at', 'updated_at']}),
    ]

    add_fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['username', 'email', 'password1', 'password2', 'role'],
        }),
    ]
