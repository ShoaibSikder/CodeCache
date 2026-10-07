from django.conf import settings
from django.db import models

from apps.common.models import BaseModel


class LearningProfile(BaseModel):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_profile')
    xp = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    last_activity_date = models.DateField(null=True, blank=True)
    last_language = models.ForeignKey('languages.Language', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')

    class Meta:
        db_table = 'learning_profile'


class TopicCompletion(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='completed_topics')
    subsection = models.ForeignKey('content.Subsection', on_delete=models.CASCADE, related_name='completions')

    class Meta:
        db_table = 'learning_topic_completion'
        constraints = [models.UniqueConstraint(fields=['user', 'subsection'], name='unique_user_topic_completion')]


class SavedContent(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_content')
    content_item = models.ForeignKey('content.ContentItem', on_delete=models.CASCADE, related_name='saved_by')

    class Meta:
        db_table = 'learning_saved_content'
        constraints = [models.UniqueConstraint(fields=['user', 'content_item'], name='unique_user_saved_content')]


class LanguageNote(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='language_notes')
    language = models.ForeignKey('languages.Language', on_delete=models.CASCADE, related_name='learner_notes')
    body = models.TextField(blank=True)

    class Meta:
        db_table = 'learning_language_note'
        constraints = [models.UniqueConstraint(fields=['user', 'language'], name='unique_user_language_note')]


class LearningActivity(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_activities')
    language = models.ForeignKey('languages.Language', null=True, blank=True, on_delete=models.SET_NULL, related_name='+')
    kind = models.CharField(max_length=30)
    action_key = models.CharField(max_length=255)
    xp_awarded = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'learning_activity'
        constraints = [models.UniqueConstraint(fields=['user', 'kind', 'action_key'], name='unique_user_learning_activity')]
