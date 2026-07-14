"""
Playground models for CodeCache.
"""

from django.db import models

from apps.common.models import BaseModel


class CodeExecution(BaseModel):
    """
    Model to store code execution history.
    """
    language = models.CharField(
        max_length=50,
        help_text="Programming language"
    )
    code = models.TextField(
        help_text="Source code that was executed"
    )
    output = models.TextField(
        blank=True,
        help_text="Execution output"
    )
    error = models.TextField(
        blank=True,
        help_text="Execution error if any"
    )
    execution_time = models.FloatField(
        null=True,
        blank=True,
        help_text="Execution time in seconds"
    )
    memory_used = models.IntegerField(
        null=True,
        blank=True,
        help_text="Memory used in KB"
    )
    status = models.CharField(
        max_length=20,
        default='pending',
        help_text="Execution status"
    )
    judge0_token = models.CharField(
        max_length=100,
        blank=True,
        help_text="Judge0 submission token"
    )

    class Meta:
        db_table = 'playground_codeexecution'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.language} execution at {self.created_at}"


class SupportedLanguage(BaseModel):
    """
    Model to store supported playground languages.
    """
    name = models.CharField(
        max_length=50,
        unique=True,
        help_text="Language name"
    )
    judge0_id = models.IntegerField(
        unique=True,
        help_text="Judge0 language ID"
    )
    version = models.CharField(
        max_length=50,
        blank=True,
        help_text="Language version"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether this language is available"
    )

    class Meta:
        db_table = 'playground_supportedlanguage'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (Judge0 ID: {self.judge0_id})"
