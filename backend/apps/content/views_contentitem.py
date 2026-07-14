"""
Views for ContentItem management.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.common.permissions import IsAdmin
from .models import ContentItem
from .serializers import (
    ContentItemSerializer,
    ContentItemCreateUpdateSerializer,
)


class ContentItemListCreateView(APIView):
    """
    GET /api/v1/admin/content-items/
    POST /api/v1/admin/content-items/
    List all content items or create new.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        content_items = (
            ContentItem.objects
            .select_related('subsection', 'subsection__section', 'subsection__section__language')
            .order_by(
                'subsection__section__language__name',
                'subsection__section__display_order',
                'subsection__display_order',
                'display_order'
            )
        )
        serializer = ContentItemSerializer(content_items, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def post(self, request):
        serializer = ContentItemCreateUpdateSerializer(data=request.data)
        if serializer.is_valid():
            content_item = serializer.save()
            return Response({
                'success': True,
                'data': ContentItemSerializer(content_item).data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to create content item.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class ContentItemDetailView(APIView):
    """
    PUT /api/v1/admin/content-items/{id}/
    DELETE /api/v1/admin/content-items/{id}/
    Update or delete a content item.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get_object(self, pk):
        try:
            return ContentItem.objects.get(pk=pk)
        except ContentItem.DoesNotExist:
            return None

    def put(self, request, pk):
        content_item = self.get_object(pk)
        if not content_item:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Content item not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = ContentItemCreateUpdateSerializer(
            content_item,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': ContentItemSerializer(content_item).data
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Failed to update content item.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        content_item = self.get_object(pk)
        if not content_item:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Content item not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        content_item.delete()
        return Response({
            'success': True,
            'data': {
                'message': 'Content item deleted successfully.'
            }
        })
