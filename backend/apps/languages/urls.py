"""
Public URL configuration for the languages app.
"""

from django.urls import path
from .views import LanguageListView, LanguageDetailView

urlpatterns = [
    path('', LanguageListView.as_view(), name='language-list'),
    path('<str:slug>/', LanguageDetailView.as_view(), name='language-detail'),
]
