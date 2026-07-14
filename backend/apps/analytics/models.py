"""
Analytics models for CodeCache.
"""

from django.db import models

from apps.common.models import BaseModel


class PageView(BaseModel):
    """
    Model to track page views.
    """
    language = models.ForeignKey(
        'languages.Language',
        on_delete=models.CASCADE,
        related_name='page_views',
        null=True,
        blank=True,
        help_text="Language that was viewed"
    )
    section = models.ForeignKey(
        'content.Section',
        on_delete=models.CASCADE,
        related_name='page_views',
        null=True,
        blank=True,
        help_text="Section that was viewed"
    )
    subsection = models.ForeignKey(
        'content.Subsection',
        on_delete=models.CASCADE,
        related_name='page_views',
        null=True,
        blank=True,
        help_text="Subsection that was viewed"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the viewer"
    )
    user_agent = models.TextField(
        blank=True,
        help_text="User agent string"
    )
    referrer = models.URLField(
        blank=True,
        help_text="Referrer URL"
    )
    path = models.CharField(
        max_length=500,
        help_text="URL path that was viewed"
    )

    class Meta:
        db_table = 'analytics_pageview'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['language', 'created_at']),
            models.Index(fields=['section', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"View: {self.path} at {self.created_at}"


class SearchQuery(BaseModel):
    """
    Model to track search queries.
    """
    query = models.CharField(
        max_length=500,
        help_text="The search query string"
    )
    results_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of results returned"
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        help_text="IP address of the searcher"
    )
    user_agent = models.TextField(
        blank=True,
        help_text="User agent string"
    )

    class Meta:
        db_table = 'analytics_searchquery'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['query', 'created_at']),
        ]

    def __str__(self):
        return f"Search: {self.query} ({self.results_count} results)"


class DailyStats(BaseModel):
    """
    Aggregated daily statistics.
    """
    date = models.DateField(
        unique=True,
        help_text="The date for these statistics"
    )
    total_views = models.PositiveIntegerField(
        default=0,
        help_text="Total page views for the day"
    )
    unique_visitors = models.PositiveIntegerField(
        default=0,
        help_text="Unique visitors for the day"
    )
    search_count = models.PositiveIntegerField(
        default=0,
        help_text="Total searches for the day"
    )
    most_viewed_language = models.ForeignKey(
        'languages.Language',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='most_viewed_days',
        help_text="Most viewed language for the day"
    )

    class Meta:
        db_table = 'analytics_dailystats'
        ordering = ['-date']

    def __str__(self):
        return f"Stats for {self.date}: {self.total_views} views"
