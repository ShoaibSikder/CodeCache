"""
Admin configuration for the content app.
"""

from django.contrib import admin
from .models import Section, Subsection, ContentItem


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'language', 'slug', 'status',
        'display_order', 'subsection_count', 'created_at'
    ]
    list_filter = ['status', 'language', 'created_at']
    search_fields = ['title', 'slug', 'description']
    ordering = ['display_order', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        (None, {'fields': ['id', 'title', 'slug']}),
        ('Relationship', {'fields': ['language']}),
        ('Details', {'fields': ['description']}),
        ('Settings', {'fields': ['status', 'display_order']}),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(Subsection)
class SubsectionAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'section', 'slug', 'status',
        'display_order', 'content_count', 'created_at'
    ]
    list_filter = ['status', 'section__language', 'created_at']
    search_fields = ['title', 'slug', 'description']
    ordering = ['display_order', 'title']
    readonly_fields = ['id', 'created_at', 'updated_at']
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = [
        (None, {'fields': ['id', 'title', 'slug']}),
        ('Relationship', {'fields': ['section']}),
        ('Details', {'fields': ['description']}),
        ('Settings', {'fields': ['status', 'display_order']}),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]


@admin.register(ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    list_display = [
        'type', 'subsection', 'status',
        'display_order', 'created_at'
    ]
    list_filter = ['type', 'status', 'created_at']
    search_fields = ['subsection__title']
    ordering = ['display_order', 'created_at']
    readonly_fields = ['id', 'created_at', 'updated_at']

    fieldsets = [
        (None, {'fields': ['id', 'type']}),
        ('Relationship', {'fields': ['subsection']}),
        ('Content', {'fields': ['data']}),
        ('Settings', {'fields': ['status', 'display_order']}),
        ('Timestamps', {
            'fields': ['created_at', 'updated_at'],
            'classes': ['collapse']
        }),
    ]
