"""
URL configuration for Section management.
"""

from django.urls import path
from .views_section import SectionListCreateView, SectionDetailView

urlpatterns = [
    path('', SectionListCreateView.as_view(), name='section-list-create'),
    path('<str:pk>/', SectionDetailView.as_view(), name='section-detail'),
]
