"""
Admin configuration for the languages app.
"""

from django.contrib import admin
from .models import Language


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'slug', 'status',
        'display_order', 'section_count', 'created_at'
    ]
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'slug', 'description']
    ordering = ['display_order', 'name']
    readonly_fields = ['id', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('name',)}

    fieldsets = [
        (None, {
            'fields': ['id', 'name', 'slug']
        }),
        ('Details', {
            'fields': ['description', 'icon']
        }),
        ('Settings', {
            'fields': ['status', 'display_order']
        }),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
