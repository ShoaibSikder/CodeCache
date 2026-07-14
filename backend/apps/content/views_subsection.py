"""
Views for Subsection management.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count, Q

from apps.common.permissions import IsAdmin, IsEditor
from .models import Subsection
from .serializers import (
    SubsectionListSerializer,
    SubsectionCreateUpdateSerializer,
)


class SubsectionListCreateView(APIView):
    """
    GET /api/v1/admin/subsections/
    POST /api/v1/admin/subsections/
    List all subsections or create new.
    """
    permission_classes = [IsAuthenticated, IsEditor]

    def get(self, request):
        subsections = (
            Subsection.objects
            .select_related('section', 'section__language')
            .annotate(
                active_content_count=Count(
                    'content_items',
                    filter=Q(content_items__status='active'),
                    distinct=True,
                )
            )
            .order_by(
                'section__language__name', 'section__display_order', 'display_order'
            )
        )
        serializer = SubsectionListSerializer(subsections, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def post(self, request):
        serializer = SubsectionCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            subsection = serializer.save()
            return Response({
                'success': True,
                'data': SubsectionListSerializer(subsection).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to create subsection.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class SubsectionDetailView(APIView):
    """
    PUT /api/v1/admin/subsections/{id}/
    DELETE /api/v1/admin/subsections/{id}/
    Update or delete a subsection.
    """
    permission_classes = [IsAuthenticated, IsEditor]

    def get_object(self, pk):
        try:
            return Subsection.objects.get(pk=pk)
        except Subsection.DoesNotExist:
            return None

    def put(self, request, pk):
        subsection = self.get_object(pk)
        if not subsection:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Subsection not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = SubsectionCreateUpdateSerializer(
            subsection,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': SubsectionListSerializer(subsection).data
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to update subsection.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        subsection = self.get_object(pk)
        if not subsection:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Subsection not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        subsection.delete()
        return Response({
            'success': True,
            'data': {
                'message': 'Subsection deleted successfully.'
            }
        })
