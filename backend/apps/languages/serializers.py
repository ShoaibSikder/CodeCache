"""
Serializers for the languages app.
"""

from rest_framework import serializers
from .models import Language


class LanguageListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing languages (lightweight).
    """
    section_count = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = [
            'id', 'name', 'slug', 'description',
            'icon', 'status', 'display_order',
            'section_count', 'created_at'
        ]

    def get_section_count(self, obj):
        annotated_count = getattr(obj, 'active_section_count', None)
        if annotated_count is not None:
            return annotated_count
        return obj.section_count


class LanguageDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for language detail with nested content.
    """
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = [
            'id', 'name', 'slug', 'description',
            'icon', 'status', 'display_order',
            'sections', 'created_at', 'updated_at'
        ]

    def get_sections(self, obj):
        """Get active sections for this language."""
        from apps.content.serializers import SectionWithContentSerializer
        sections = getattr(obj, 'active_sections', None)
        if sections is None:
            sections = obj.sections.filter(status='active').order_by('display_order')
        return SectionWithContentSerializer(sections, many=True).data


class LanguageCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating and updating languages.
    """

    class Meta:
        model = Language
        fields = [
            'name', 'slug', 'description',
            'icon', 'status', 'display_order'
        ]

    def validate_slug(self, value):
        """Ensure slug is unique."""
        instance = self.instance
        queryset = Language.objects.filter(slug=value)
        if instance:
            queryset = queryset.exclude(pk=instance.pk)
        if queryset.exists():
            raise serializers.ValidationError(
                'A language with this slug already exists.'
            )
        return value
