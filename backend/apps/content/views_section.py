"""
Views for Section management.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q

from apps.common.permissions import IsAdmin
from .models import Section
from .serializers import (
    SectionListSerializer,
    SectionCreateUpdateSerializer,
)


class SectionListCreateView(APIView):
    """
    GET /api/v1/admin/sections/
    POST /api/v1/admin/sections/
    List all sections or create new.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        sections = (
            Section.objects
            .select_related('language')
            .annotate(
                active_subsection_count=Count(
                    'subsections',
                    filter=Q(subsections__status='active'),
                    distinct=True,
                )
            )
            .order_by('language__name', 'display_order')
        )
        serializer = SectionListSerializer(sections, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def post(self, request):
        serializer = SectionCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            section = serializer.save()
            return Response({
                'success': True,
                'data': SectionListSerializer(section).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to create section.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class SectionDetailView(APIView):
    """
    PUT /api/v1/admin/sections/{id}/
    DELETE /api/v1/admin/sections/{id}/
    Update or delete a section.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        try:
            return Section.objects.get(pk=pk)
        except Section.DoesNotExist:
            return None

    def put(self, request, pk):
        section = self.get_object(pk)
        if not section:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Section not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SectionCreateUpdateSerializer(
            section,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': SectionListSerializer(section).data
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to update section.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        section = self.get_object(pk)
        if not section:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Section not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        section.delete()
        return Response({
            'success': True,
            'data': {
                'message': 'Section deleted successfully.'
            }
        })
