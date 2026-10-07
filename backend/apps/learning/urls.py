from django.urls import path

from .views import (
    ActivityView,
    LastLanguageView,
    LearningOverviewView,
    NoteView,
    SavedContentView,
    TopicCompletionView,
)

urlpatterns = [
    path('overview/', LearningOverviewView.as_view()),
    path('topics/<uuid:subsection_id>/complete/', TopicCompletionView.as_view()),
    path('saved/', SavedContentView.as_view()),
    path('notes/<slug:language_slug>/', NoteView.as_view()),
    path('activities/', ActivityView.as_view()),
    path('last-language/', LastLanguageView.as_view()),
]
