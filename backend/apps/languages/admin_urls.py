"""
Admin URL configuration for the languages app.
"""

from django.urls import path
from .views import AdminLanguageListCreateView, AdminLanguageDetailView

urlpatterns = [
    path('', AdminLanguageListCreateView.as_view(), name='admin-language-list-create'),
    path('<str:pk>/', AdminLanguageDetailView.as_view(), name='admin-language-detail'),
]
