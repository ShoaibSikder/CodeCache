"""
Language model for CodeCache.
"""

from django.db import models

from apps.common.models import BaseModel
from apps.common.constants import Status
from apps.common.validators import validate_slug


class Language(BaseModel):
    """
    Programming language model.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Language name (e.g., Python, JavaScript)"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        validators=[validate_slug],
        help_text="URL-friendly identifier"
    )
    description = models.TextField(
        blank=True,
        help_text="Brief description of the language"
    )
    icon = models.ImageField(
        upload_to='languages/icons/',
        blank=True,
        null=True,
        help_text="Language icon image"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.CHOICES,
        default=Status.ACTIVE,
        db_index=True,
        help_text="Publication status"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Order for display"
    )

    class Meta:
        db_table = 'languages_language'
        ordering = ['display_order', 'name']
        verbose_name = 'Language'
        verbose_name_plural = 'Languages'

    def __str__(self):
        return self.name

    @property
    def section_count(self):
        """Return the number of sections for this language."""
        return self.sections.filter(status=Status.ACTIVE).count()

    @property
    def is_active_status(self):
        """Check if the language is active."""
        return self.status == Status.ACTIVE
