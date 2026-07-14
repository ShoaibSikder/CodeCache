"""
URL configuration for Subsection management.
"""

from django.urls import path
from .views_subsection import SubsectionListCreateView, SubsectionDetailView

urlpatterns = [
    path('', SubsectionListCreateView.as_view(), name='subsection-list-create'),
    path('<str:pk>/', SubsectionDetailView.as_view(), name='subsection-detail'),
]
