"""
Admin configuration for the playground app.
"""

from django.contrib import admin
from .models import CodeExecution, SupportedLanguage


@admin.register(CodeExecution)
class CodeExecutionAdmin(admin.ModelAdmin):
    list_display = ['language', 'status', 'execution_time', 'created_at']
    list_filter = ['language', 'status', 'created_at']
    search_fields = ['code', 'output', 'error']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'


@admin.register(SupportedLanguage)
class SupportedLanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'judge0_id', 'version', 'is_active']
    list_filter = ['is_active']
    search_fields = ['name']
    readonly_fields = ['id', 'created_at', 'updated_at']
