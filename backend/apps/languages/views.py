"""
Views for the languages app.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.db.models import Count, Prefetch, Q

from apps.common.permissions import IsAdmin
from apps.content.models import Section, Subsection, ContentItem
from .models import Language
from .serializers import (
    LanguageListSerializer,
    LanguageDetailSerializer,
    LanguageCreateUpdateSerializer,
)


class LanguageListView(APIView):
    """
    GET /api/v1/languages/
    List all active languages (public).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        languages = (
            Language.objects
            .filter(status='active')
            .annotate(
                active_section_count=Count(
                    'sections',
                    filter=Q(sections__status='active'),
                    distinct=True,
                )
            )
            .order_by('display_order', 'name')
        )
        serializer = LanguageListSerializer(languages, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class LanguageDetailView(APIView):
    """
    GET /api/v1/languages/{slug}/
    Get a single language with full nested content (public).
    """
    permission_classes = [AllowAny]

    def get(self, request, slug):
        active_content_items = Prefetch(
            'content_items',
            queryset=ContentItem.objects.filter(status='active').order_by('display_order', 'created_at'),
            to_attr='active_content_items',
        )
        active_subsections = Prefetch(
            'subsections',
            queryset=(
                Subsection.objects
                .filter(status='active')
                .prefetch_related(active_content_items)
                .order_by('display_order', 'title')
            ),
            to_attr='active_subsections',
        )
        active_sections = Prefetch(
            'sections',
            queryset=(
                Section.objects
                .filter(status='active')
                .prefetch_related(active_subsections)
                .order_by('display_order', 'title')
            ),
            to_attr='active_sections',
        )

        try:
            language = (
                Language.objects
                .prefetch_related(active_sections)
                .get(slug=slug, status='active')
            )
        except Language.DoesNotExist:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Language not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = LanguageDetailSerializer(language)
        return Response({
            'success': True,
            'data': serializer.data
        })


class AdminLanguageListCreateView(APIView):
    """
    GET /api/v1/admin/languages/
    POST /api/v1/admin/languages/
    Admin: List all languages (including inactive) or create new.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        languages = (
            Language.objects
            .annotate(
                active_section_count=Count(
                    'sections',
                    filter=Q(sections__status='active'),
                    distinct=True,
                )
            )
            .order_by('display_order', 'name')
        )
        serializer = LanguageListSerializer(languages, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def post(self, request):
        serializer = LanguageCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            language = serializer.save()
            return Response({
                'success': True,
                'data': LanguageListSerializer(language).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to create language.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class AdminLanguageDetailView(APIView):
    """
    PUT /api/v1/admin/languages/{id}/
    DELETE /api/v1/admin/languages/{id}/
    Admin: Update or delete a language.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        try:
            return Language.objects.get(pk=pk)
        except Language.DoesNotExist:
            return None

    def put(self, request, pk):
        language = self.get_object(pk)
        if not language:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Language not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = LanguageCreateUpdateSerializer(
            language,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': LanguageListSerializer(language).data
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to update language.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        language = self.get_object(pk)
        if not language:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Language not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        language.delete()
        return Response({
            'success': True,
            'data': {
                'message': 'Language deleted successfully.'
            }
        }, status=status.HTTP_200_OK)
