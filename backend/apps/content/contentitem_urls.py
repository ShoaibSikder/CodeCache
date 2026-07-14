"""
URL configuration for ContentItem management.
"""

from django.urls import path
from .views_contentitem import ContentItemListCreateView, ContentItemDetailView

urlpatterns = [
    path('', ContentItemListCreateView.as_view(), name='contentitem-list-create'),
    path('<str:pk>/', ContentItemDetailView.as_view(), name='contentitem-detail'),
]
