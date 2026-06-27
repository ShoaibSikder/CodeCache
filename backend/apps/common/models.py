"""
Base model with UUID primary key for all CodeCache models.
"""

import uuid
from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model that provides UUID primary key and timestamp fields.
    All models in CodeCache inherit from this.
    """
    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True,
        help_text="Unique identifier (UUID v4)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text="Timestamp when the record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated"
    )

    class Meta:
        abstract = True
        ordering = ['-created_at']
