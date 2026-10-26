"""
Admin configuration for the playground app.
"""

from django.contrib import admin
from .models import CodeExecution


@admin.register(CodeExecution)
class CodeExecutionAdmin(admin.ModelAdmin):
    list_display = ['language', 'status', 'execution_time', 'created_at']
    list_filter = ['language', 'status', 'created_at']
    search_fields = ['code', 'output', 'error']
    readonly_fields = ['id', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
