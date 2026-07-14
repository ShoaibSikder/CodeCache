"""
URL configuration for the search app.
"""

from django.urls import path
from .views import SearchView, SearchSuggestionsView

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('suggestions/', SearchSuggestionsView.as_view(), name='search-suggestions'),
]
