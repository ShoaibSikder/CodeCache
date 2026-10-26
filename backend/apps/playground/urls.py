"""
URL configuration for the playground app.
"""

from django.urls import path
from .views import RunCodeView, SupportedLanguagesView

urlpatterns = [
    path('run/', RunCodeView.as_view(), name='run-code'),
    path('languages/', SupportedLanguagesView.as_view(), name='supported-languages'),
]
