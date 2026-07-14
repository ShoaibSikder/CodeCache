"""
Search views for CodeCache using database-agnostic text search.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.db.models import Q

from apps.languages.models import Language
from apps.content.models import Section, Subsection, ContentItem
from apps.common.constants import SEARCH_MIN_QUERY_LENGTH, SEARCH_MAX_RESULTS


class SearchView(APIView):
    """
    GET /api/v1/search/?q=python
    Full-text search across languages, sections, subsections, and content items.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query_text = request.query_params.get('q', '').strip()

        if not query_text:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Search query is required. Use ?q=your_query'
                },
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        if len(query_text) < SEARCH_MIN_QUERY_LENGTH:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': f'Search query must be at least {SEARCH_MIN_QUERY_LENGTH} characters long.'
                },
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        results = self.perform_search(query_text)

        return Response({
            'success': True,
            'data': {
                'query': query_text,
                'total_results': results['total'],
                'results': results['flat'],
                'grouped': {
                    'languages': results['languages'],
                    'sections': results['sections'],
                    'subsections': results['subsections'],
                    'content_items': results['content_items'],
                }
            }
        })

    def perform_search(self, query_text):
        """
        Perform text search across all content types using icontains.
        """
        # Search Languages
        languages = self.search_languages(query_text)

        # Search Sections
        sections = self.search_sections(query_text)

        # Search Subsections
        subsections = self.search_subsections(query_text)

        # Search Content Items (for code and text content)
        content_items = self.search_content_items(query_text)

        total = (
            len(languages) +
            len(sections) +
            len(subsections) +
            len(content_items)
        )

        return {
            'languages': languages,
            'sections': sections,
            'subsections': subsections,
            'content_items': content_items,
            'total': total,
            'flat': languages + sections + subsections + content_items
        }

    def search_languages(self, query_text):
        """Search languages by name, description."""
        results = Language.objects.filter(status='active').filter(
            Q(name__icontains=query_text) |
            Q(description__icontains=query_text) |
            Q(slug__icontains=query_text)
        )[:SEARCH_MAX_RESULTS]

        return [
            {
                'id': str(lang.id),
                'type': 'language',
                'name': lang.name,
                'slug': lang.slug,
                'description': lang.description[:200] if lang.description else '',
                'url': f'/languages/{lang.slug}/',
            }
            for lang in results
        ]

    def search_sections(self, query_text):
        """Search sections by title, description."""
        results = Section.objects.filter(status='active').filter(
            Q(title__icontains=query_text) |
            Q(description__icontains=query_text) |
            Q(slug__icontains=query_text)
        ).select_related('language')[:SEARCH_MAX_RESULTS]

        return [
            {
                'id': str(sec.id),
                'type': 'section',
                'title': sec.title,
                'slug': sec.slug,
                'description': sec.description[:200] if sec.description else '',
                'language': {
                    'name': sec.language.name,
                    'slug': sec.language.slug
                },
                'url': f'/languages/{sec.language.slug}/#{sec.slug}',
            }
            for sec in results
        ]

    def search_subsections(self, query_text):
        """Search subsections by title, description."""
        results = Subsection.objects.filter(status='active').filter(
            Q(title__icontains=query_text) |
            Q(description__icontains=query_text) |
            Q(slug__icontains=query_text)
        ).select_related('section__language')[:SEARCH_MAX_RESULTS]

        return [
            {
                'id': str(sub.id),
                'type': 'subsection',
                'title': sub.title,
                'slug': sub.slug,
                'description': sub.description[:200] if sub.description else '',
                'section': {
                    'title': sub.section.title,
                    'slug': sub.section.slug
                },
                'language': {
                    'name': sub.section.language.name,
                    'slug': sub.section.language.slug
                },
                'url': f'/languages/{sub.section.language.slug}/#{sub.slug}',
            }
            for sub in results
        ]

    def search_content_items(self, query_text):
        """Search content items by their data content."""
        results = ContentItem.objects.filter(status='active').filter(
            Q(data__icontains=query_text)
        ).select_related(
            'subsection__section__language'
        ).order_by('display_order')[:SEARCH_MAX_RESULTS]

        return [
            {
                'id': str(item.id),
                'type': 'content',
                'content_type': item.type,
                'subsection': {
                    'title': item.subsection.title,
                    'slug': item.subsection.slug
                },
                'section': {
                    'title': item.subsection.section.title,
                    'slug': item.subsection.section.slug
                },
                'language': {
                    'name': item.subsection.section.language.name,
                    'slug': item.subsection.section.language.slug
                },
                'preview': self.get_content_preview(item, query_text),
                'url': f'/languages/{item.subsection.section.language.slug}/',
            }
            for item in results
        ]

    def get_content_preview(self, content_item, query_text):
        """Generate a preview snippet for the content item."""
        data = content_item.data
        preview = ''

        if content_item.type == 'paragraph' and 'text' in data:
            preview = data['text']
        elif content_item.type == 'code' and 'code' in data:
            preview = data['code'][:200]
        elif content_item.type == 'heading' and 'text' in data:
            preview = data['text']
        elif content_item.type == 'note' and 'text' in data:
            preview = data['text']
        elif content_item.type == 'table' and 'rows' in data:
            preview = f"Table with columns: {', '.join(data.get('columns', []))}"
        else:
            preview = str(data)[:200]

        # Highlight the query term
        import re
        highlighted = re.sub(
            f'({re.escape(query_text)})',
            r'<mark>\1</mark>',
            preview,
            flags=re.IGNORECASE
        )

        return highlighted[:300]


class SearchSuggestionsView(APIView):
    """
    GET /api/v1/search/suggestions/?q=py
    Get search suggestions as user types.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        query_text = request.query_params.get('q', '').strip().lower()

        if len(query_text) < 1:
            return Response({
                'success': True,
                'data': []
            })

        suggestions = []

        # Language name suggestions
        languages = Language.objects.filter(
            status='active',
            name__icontains=query_text
        ).values('name', 'slug', 'description')[:5]
        suggestions.extend([
            {
                'type': 'language',
                'text': item['name'],
                'url': f"/language/{item['slug']}",
                'subtitle': (item['description'] or '')[:80]
            }
            for item in languages
        ])

        # Section title suggestions
        sections = Section.objects.filter(
            status='active',
            title__icontains=query_text
        ).values('title', 'slug', 'language__slug')[:5]
        suggestions.extend([
            {
                'type': 'section',
                'text': item['title'],
                'url': f"/languages/{item['language__slug']}/#{item['slug']}",
                'subtitle': ''
            }
            for item in sections
        ])

        # Subsection title suggestions
        subsections = Subsection.objects.filter(
            status='active',
            title__icontains=query_text
        ).values('title', 'slug', 'section__slug', 'section__language__slug')[:5]
        suggestions.extend([
            {
                'type': 'subsection',
                'text': item['title'],
                'url': f"/languages/{item['section__language__slug']}/#{item['slug']}",
                'subtitle': ''
            }
            for item in subsections
        ])

        return Response({
            'success': True,
            'data': suggestions[:10]
        })