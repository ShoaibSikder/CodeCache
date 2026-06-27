"""
Pagination classes for CodeCache.
"""

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from .constants import DEFAULT_PAGE_SIZE, MAX_PAGE_SIZE


class StandardPagination(PageNumberPagination):
    """
    Standard pagination with configurable page size.
    """
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = 'page_size'
    max_page_size = MAX_PAGE_SIZE

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'page': self.page.number,
            'page_size': self.get_page_size(self.request),
            'total_pages': self.page.paginator.num_pages,
            'results': data,
        })
