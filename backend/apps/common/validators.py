"""
Shared validators for CodeCache.
"""

import re
from django.core.exceptions import ValidationError


def validate_slug(value):
    """
    Validate that a slug contains only lowercase letters, numbers, and hyphens.
    """
    if not re.match(r'^[a-z0-9-]+$', value):
        raise ValidationError(
            'Slug can only contain lowercase letters, numbers, and hyphens.'
        )
    if value.startswith('-') or value.endswith('-'):
        raise ValidationError(
            'Slug cannot start or end with a hyphen.'
        )
    if '--' in value:
        raise ValidationError(
            'Slug cannot contain consecutive hyphens.'
        )


def validate_username(value):
    """
    Validate username format.
    """
    if not re.match(r'^[a-zA-Z0-9_-]+$', value):
        raise ValidationError(
            'Username can only contain letters, numbers, underscores, and hyphens.'
        )
    if len(value) < 3:
        raise ValidationError(
            'Username must be at least 3 characters long.'
        )


def validate_display_order(value):
    """
    Validate display order is a positive integer.
    """
    if value < 0:
        raise ValidationError(
            'Display order must be a non-negative integer.'
        )


def validate_content_data(value):
    """
    Validate content item data JSON structure.
    Ensures the data has the required fields based on content type.
    """
    if not isinstance(value, dict):
        raise ValidationError('Content data must be a JSON object.')
