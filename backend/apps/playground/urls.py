"""
URL configuration for the playground app.
"""

from django.urls import path
from .views import RunCodeView, SupportedLanguagesView, ExecutionStatusView

urlpatterns = [
    path('run/', RunCodeView.as_view(), name='run-code'),
    path('languages/', SupportedLanguagesView.as_view(), name='supported-languages'),
    path('status/<str:token>/', ExecutionStatusView.as_view(), name='execution-status'),
]
