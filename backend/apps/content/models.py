"""
Content models for CodeCache - Section, Subsection, and ContentItem.
"""

from django.db import models

from apps.common.models import BaseModel
from apps.common.constants import Status, ContentType
from apps.common.validators import validate_slug


class Section(BaseModel):
    """
    Section model - top-level organization under a Language.
    """
    language = models.ForeignKey(
        'languages.Language',
        on_delete=models.CASCADE,
        related_name='sections',
        help_text="The language this section belongs to"
    )
    title = models.CharField(
        max_length=200,
        help_text="Section title"
    )
    slug = models.SlugField(
        max_length=200,
        validators=[validate_slug],
        help_text="URL-friendly identifier"
    )
    description = models.TextField(
        blank=True,
        help_text="Section description"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Order for display"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.CHOICES,
        default=Status.ACTIVE,
        db_index=True,
        help_text="Publication status"
    )

    class Meta:
        db_table = 'content_section'
        ordering = ['display_order', 'title']
        verbose_name = 'Section'
        verbose_name_plural = 'Sections'
        unique_together = ['language', 'slug']

    def __str__(self):
        return f"{self.language.name} > {self.title}"

    @property
    def subsection_count(self):
        """Return the number of subsections for this section."""
        return self.subsections.filter(status=Status.ACTIVE).count()


class Subsection(BaseModel):
    """
    Subsection model - second-level organization under a Section.
    """
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        related_name='subsections',
        help_text="The section this subsection belongs to"
    )
    title = models.CharField(
        max_length=200,
        help_text="Subsection title"
    )
    slug = models.SlugField(
        max_length=200,
        validators=[validate_slug],
        help_text="URL-friendly identifier"
    )
    description = models.TextField(
        blank=True,
        help_text="Subsection description"
    )
    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Order for display"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.CHOICES,
        default=Status.ACTIVE,
        db_index=True,
        help_text="Publication status"
    )

    class Meta:
        db_table = 'content_subsection'
        ordering = ['display_order', 'title']
        verbose_name = 'Subsection'
        verbose_name_plural = 'Subsections'
        unique_together = ['section', 'slug']

    def __str__(self):
        return f"{self.section.title} > {self.title}"

    @property
    def content_count(self):
        """Return the number of content items for this subsection."""
        return self.content_items.filter(status=Status.ACTIVE).count()

    @property
    def language(self):
        """Get the parent language."""
        return self.section.language


class ContentItem(BaseModel):
    """
    Content Item model - stores all documentation content.
    Uses a flexible JSONField for data to support multiple content types.
    """
    subsection = models.ForeignKey(
        Subsection,
        on_delete=models.CASCADE,
        related_name='content_items',
        help_text="The subsection this content belongs to"
    )
    type = models.CharField(
        max_length=20,
        choices=ContentType.ALL_CHOICES,
        db_index=True,
        help_text="Type of content"
    )
    data = models.JSONField(
        help_text="Content data in JSON format",
        default=dict
    )
    display_order = models.PositiveIntegerField(
        default=0,
        db_index=True,
        help_text="Order for display"
    )
    status = models.CharField(
        max_length=20,
        choices=Status.CHOICES,
        default=Status.ACTIVE,
        db_index=True,
        help_text="Publication status"
    )

    class Meta:
        db_table = 'content_contentitem'
        ordering = ['display_order', 'created_at']
        verbose_name = 'Content Item'
        verbose_name_plural = 'Content Items'

    def __str__(self):
        return f"{self.subsection.title} > {self.type}"

    @property
    def language(self):
        """Get the parent language."""
        return self.subsection.section.language

    @property
    def section(self):
        """Get the parent section."""
        return self.subsection.section
