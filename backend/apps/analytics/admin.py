"""
Admin configuration for the analytics app.
"""

from django.contrib import admin
from .models import PageView, SearchQuery, DailyStats


@admin.register(PageView)
class PageViewAdmin(admin.ModelAdmin):
    list_display = ['path', 'language', 'ip_address', 'created_at']
    list_filter = ['created_at']
    search_fields = ['path', 'ip_address']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ['query', 'results_count', 'created_at']
    search_fields = ['query']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(DailyStats)
class DailyStatsAdmin(admin.ModelAdmin):
    list_display = ['date', 'total_views', 'unique_visitors', 'search_count']
    ordering = ['-date']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'date'
