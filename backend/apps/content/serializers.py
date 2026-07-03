"""
Serializers for the content app.
"""

from rest_framework import serializers
from .models import Section, Subsection, ContentItem
from apps.languages.models import Language


class ContentItemSerializer(serializers.ModelSerializer):
    """
    Serializer for ContentItem.
    """
    subsection = serializers.PrimaryKeyRelatedField(read_only=True)
    subsection_name = serializers.SerializerMethodField()

    class Meta:
        model = ContentItem
        fields = [
            'id', 'subsection', 'subsection_name', 'type', 'data',
            'display_order', 'status', 'created_at'
        ]

    def get_subsection_name(self, obj):
        return obj.subsection.title


class ContentItemCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating ContentItem.
    """
    class Meta:
        model = ContentItem
        fields = [
            'subsection', 'type', 'data',
            'display_order', 'status'
        ]

    def validate_data(self, value):
        """Validate content data based on type."""
        if not isinstance(value, dict):
            raise serializers.ValidationError('Content data must be a JSON object.')
        return value


class SubsectionListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing subsections.
    """
    content_count = serializers.SerializerMethodField()
    section = serializers.PrimaryKeyRelatedField(read_only=True)
    section_name = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = [
            'id', 'section', 'section_name', 'title', 'slug', 'description',
            'display_order', 'status', 'content_count',
            'created_at'
        ]

    def get_section_name(self, obj):
        return obj.section.title

    def get_content_count(self, obj):
        annotated_count = getattr(obj, 'active_content_count', None)
        if annotated_count is not None:
            return annotated_count
        return obj.content_count


class SubsectionWithContentSerializer(serializers.ModelSerializer):
    """
    Serializer for subsection with nested content items.
    """
    content_items = serializers.SerializerMethodField()

    class Meta:
        model = Subsection
        fields = [
            'id', 'title', 'slug', 'description',
            'display_order', 'status', 'content_items',
            'created_at'
        ]

    def get_content_items(self, obj):
        """Get active content items for this subsection."""
        items = getattr(obj, 'active_content_items', None)
        if items is None:
            items = obj.content_items.filter(status='active').order_by('display_order')
        return ContentItemSerializer(items, many=True).data


class SubsectionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating subsections.
    """
    class Meta:
        model = Subsection
        fields = [
            'section', 'title', 'slug',
            'description', 'display_order', 'status'
        ]

    def validate(self, data):
        """Ensure unique slug within section."""
        section = data.get('section')
        slug = data.get('slug')
        instance = self.instance

        if section and slug:
            queryset = Subsection.objects.filter(section=section, slug=slug)
            if instance:
                queryset = queryset.exclude(pk=instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({
                    'slug': 'A subsection with this slug already exists in this section.'
                })
        return data


class SectionListSerializer(serializers.ModelSerializer):
    """
    Serializer for listing sections.
    """
    subsection_count = serializers.SerializerMethodField()
    language = serializers.PrimaryKeyRelatedField(read_only=True)
    language_name = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = [
            'id', 'language', 'language_name', 'title', 'slug', 'description',
            'display_order', 'status', 'subsection_count',
            'created_at'
        ]

    def get_language_name(self, obj):
        return obj.language.name

    def get_subsection_count(self, obj):
        annotated_count = getattr(obj, 'active_subsection_count', None)
        if annotated_count is not None:
            return annotated_count
        return obj.subsection_count


class SectionWithContentSerializer(serializers.ModelSerializer):
    """
    Serializer for section with nested subsections and content.
    """
    subsections = serializers.SerializerMethodField()

    class Meta:
        model = Section
        fields = [
            'id', 'title', 'slug', 'description',
            'display_order', 'status', 'subsections',
            'created_at'
        ]

    def get_subsections(self, obj):
        """Get active subsections with content for this section."""
        subsections = getattr(obj, 'active_subsections', None)
        if subsections is None:
            subsections = obj.subsections.filter(status='active').order_by('display_order')
        return SubsectionWithContentSerializer(subsections, many=True).data


class SectionCreateUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating/updating sections.
    """
    class Meta:
        model = Section
        fields = [
            'language', 'title', 'slug',
            'description', 'display_order', 'status'
        ]

    def validate(self, data):
        """Ensure unique slug within language."""
        language = data.get('language')
        slug = data.get('slug')
        instance = self.instance

        if language and slug:
            queryset = Section.objects.filter(language=language, slug=slug)
            if instance:
                queryset = queryset.exclude(pk=instance.pk)
            if queryset.exists():
                raise serializers.ValidationError({
                    'slug': 'A section with this slug already exists in this language.'
                })
        return data


class ContentTreeSerializer(serializers.ModelSerializer):
    """
    Full content tree serializer for a language.
    Returns the complete hierarchy: Language -> Sections -> Subsections -> Content Items.
    """
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Language
        fields = [
            'id', 'name', 'slug', 'description',
            'icon', 'status', 'sections'
        ]

    def get_sections(self, obj):
        """Get all active sections with full nested content."""
        sections = getattr(obj, 'active_sections', None)
        if sections is None:
            sections = obj.sections.filter(status='active').order_by('display_order')
        return SectionWithContentSerializer(sections, many=True).data
