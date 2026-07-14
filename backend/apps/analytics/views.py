"""
Analytics views for CodeCache.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.utils import timezone
from django.db.models import Count, Q
from datetime import timedelta

from apps.common.permissions import IsAdmin
from .models import PageView, SearchQuery, DailyStats


class TrackView(APIView):
    """
    POST /api/v1/analytics/view/
    Track a page view.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        language_id = data.get('language_id')
        section_id = data.get('section_id')
        subsection_id = data.get('subsection_id')
        path = data.get('path', '')
        referrer = data.get('referrer', '')

        # Get client info
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        page_view = PageView.objects.create(
            language_id=language_id if language_id else None,
            section_id=section_id if section_id else None,
            subsection_id=subsection_id if subsection_id else None,
            path=path,
            referrer=referrer,
            ip_address=ip_address,
            user_agent=user_agent
        )

        return Response({
            'success': True,
            'data': {
                'id': str(page_view.id),
                'message': 'View tracked successfully.'
            }
        }, status=status.HTTP_201_CREATED)


class TrackSearch(APIView):
    """
    POST /api/v1/analytics/search/
    Track a search query.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data

        query = data.get('query', '').strip()
        results_count = data.get('results_count', 0)

        if not query:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Search query is required.'
                },
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get client info
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip_address = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR')
        user_agent = request.META.get('HTTP_USER_AGENT', '')

        search_query = SearchQuery.objects.create(
            query=query,
            results_count=results_count,
            ip_address=ip_address,
            user_agent=user_agent
        )

        return Response({
            'success': True,
            'data': {
                'id': str(search_query.id),
                'message': 'Search tracked successfully.'
            }
        }, status=status.HTTP_201_CREATED)


class DashboardStatsView(APIView):
    """
    GET /api/v1/admin/analytics/
    Admin: Get dashboard analytics statistics.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        now = timezone.now()
        today = now.date()
        yesterday = today - timedelta(days=1)
        last_7_days = today - timedelta(days=7)
        last_30_days = today - timedelta(days=30)

        # Today's stats
        today_views = PageView.objects.filter(created_at__date=today).count()
        yesterday_views = PageView.objects.filter(created_at__date=yesterday).count()

        # Views trend (last 7 days)
        daily_views = []
        for i in range(6, -1, -1):
            date = today - timedelta(days=i)
            count = PageView.objects.filter(created_at__date=date).count()
            daily_views.append({
                'date': date.isoformat(),
                'views': count
            })

        # Top languages
        top_languages = PageView.objects.filter(
            created_at__date__gte=last_7_days,
            language__isnull=False
        ).values(
            'language__name',
            'language__slug'
        ).annotate(
            view_count=Count('id')
        ).order_by('-view_count')[:10]

        # Top sections
        top_sections = PageView.objects.filter(
            created_at__date__gte=last_7_days,
            section__isnull=False
        ).values(
            'section__title',
            'section__slug',
            'section__language__name',
            'section__language__slug'
        ).annotate(
            view_count=Count('id')
        ).order_by('-view_count')[:10]

        # Top searches
        top_searches = SearchQuery.objects.filter(
            created_at__date__gte=last_7_days
        ).values('query').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        # Monthly stats
        total_month_views = PageView.objects.filter(created_at__date__gte=last_30_days).count()
        total_month_searches = SearchQuery.objects.filter(created_at__date__gte=last_30_days).count()

        # Unique visitors estimate (by distinct IP)
        unique_visitors_today = PageView.objects.filter(
            created_at__date=today
        ).values('ip_address').distinct().count()

        unique_visitors_month = PageView.objects.filter(
            created_at__date__gte=last_30_days
        ).values('ip_address').distinct().count()

        # Per-language statistics
        language_stats = PageView.objects.filter(
            created_at__date__gte=last_30_days,
            language__isnull=False
        ).values(
            'language__name',
            'language__slug',
            'language__id'
        ).annotate(
            view_count=Count('id'),
            unique_visitors=Count('ip_address', distinct=True)
        ).order_by('-view_count')

        return Response({
            'success': True,
            'data': {
                'overview': {
                    'today_views': today_views,
                    'yesterday_views': yesterday_views,
                    'views_change_percent': self.calculate_change_percent(today_views, yesterday_views),
                    'unique_visitors_today': unique_visitors_today,
                    'unique_visitors_month': unique_visitors_month,
                    'total_month_views': total_month_views,
                    'total_month_searches': total_month_searches,
                },
                'daily_views': daily_views,
                'top_languages': list(top_languages),
                'top_sections': list(top_sections),
                'top_searches': list(top_searches),
                'language_stats': list(language_stats),
            }
        })

    def calculate_change_percent(self, today, yesterday):
        """Calculate percentage change between today and yesterday."""
        if yesterday == 0:
            return 100 if today > 0 else 0
        return round(((today - yesterday) / yesterday) * 100, 1)


class PopularContentView(APIView):
    """
    GET /api/v1/analytics/popular/
    Get popular content (public endpoint).
    """
    permission_classes = [AllowAny]

    def get(self, request):
        now = timezone.now()
        last_7_days = now.date() - timedelta(days=7)

        # Popular languages
        popular_languages = PageView.objects.filter(
            created_at__date__gte=last_7_days,
            language__isnull=False
        ).values(
            'language__name',
            'language__slug',
            'language__icon'
        ).annotate(
            view_count=Count('id')
        ).order_by('-view_count')[:5]

        # Popular sections
        popular_sections = PageView.objects.filter(
            created_at__date__gte=last_7_days,
            section__isnull=False
        ).values(
            'section__title',
            'section__slug',
            'section__language__name',
            'section__language__slug'
        ).annotate(
            view_count=Count('id')
        ).order_by('-view_count')[:5]

        return Response({
            'success': True,
            'data': {
                'popular_languages': list(popular_languages),
                'popular_sections': list(popular_sections),
            }
        })
