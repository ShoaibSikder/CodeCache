"""
URL configuration for the analytics app.
"""

from django.urls import path
from .views import (
    TrackView,
    TrackSearch,
    DashboardStatsView,
    PopularContentView,
)

urlpatterns = [
    path('view/', TrackView.as_view(), name='track-view'),
    path('search/', TrackSearch.as_view(), name='track-search'),
    path('popular/', PopularContentView.as_view(), name='popular-content'),
    path('', DashboardStatsView.as_view(), name='dashboard-stats'),
]
