from datetime import timedelta

from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.content.models import ContentItem, Subsection
from apps.languages.models import Language
from .models import LanguageNote, LearningActivity, LearningProfile, SavedContent, TopicCompletion

XP_BY_ACTIVITY = {'daily_challenge': 90, 'bug_fix': 60, 'quiz': 75, 'note': 15}


def profile_for(user):
    return LearningProfile.objects.get_or_create(user=user)[0]


class LearningOverviewView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = profile_for(request.user)
        completed_ids = TopicCompletion.objects.filter(user=request.user).values_list('subsection_id', flat=True)
        saved_ids = SavedContent.objects.filter(user=request.user).values_list('content_item_id', flat=True)
        return Response({'success': True, 'data': {
            'xp': profile.xp,
            'streak': profile.current_streak,
            'last_language_slug': profile.last_language.slug if profile.last_language else None,
            'completed_subsection_ids': [str(item) for item in completed_ids],
            'saved_content_item_ids': [str(item) for item in saved_ids],
        }})


class TopicCompletionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, subsection_id):
        subsection = get_object_or_404(Subsection, pk=subsection_id, status='active')
        _, created = TopicCompletion.objects.get_or_create(user=request.user, subsection=subsection)
        profile = profile_for(request.user)
        if created:
            profile.xp += 20
            profile.save(update_fields=['xp', 'updated_at'])
        return Response({'success': True, 'data': {'completed': True, 'xp': profile.xp, 'awarded_xp': 20 if created else 0}})


class SavedContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        saved = SavedContent.objects.filter(user=request.user).select_related('content_item__subsection__section__language')
        items = []
        for entry in saved:
            item = entry.content_item
            data = item.data or {}
            items.append({
                'id': str(item.id), 'saved_id': str(entry.id), 'title': data.get('title') or item.subsection.title,
                'category': item.subsection.section.title, 'language': item.subsection.section.language.slug,
                'code': data.get('code', ''),
            })
        return Response({'success': True, 'data': items})

    def post(self, request):
        content_item = get_object_or_404(ContentItem, pk=request.data.get('content_item_id'), status='active')
        entry, created = SavedContent.objects.get_or_create(user=request.user, content_item=content_item)
        if not created:
            entry.delete()
        return Response({'success': True, 'data': {'saved': created, 'content_item_id': str(content_item.id)}})


class NoteView(APIView):
    permission_classes = [IsAuthenticated]

    def get_language(self, language_slug):
        return get_object_or_404(Language, slug=language_slug, status='active')

    def get(self, request, language_slug):
        note = LanguageNote.objects.filter(user=request.user, language=self.get_language(language_slug)).first()
        return Response({'success': True, 'data': {'body': note.body if note else ''}})

    def put(self, request, language_slug):
        language = self.get_language(language_slug)
        body = str(request.data.get('body', ''))
        note, created = LanguageNote.objects.update_or_create(user=request.user, language=language, defaults={'body': body})
        profile = profile_for(request.user)
        if created and body.strip():
            LearningActivity.objects.get_or_create(user=request.user, language=language, kind='note', action_key=language.slug, defaults={'xp_awarded': XP_BY_ACTIVITY['note']})
            profile.xp += XP_BY_ACTIVITY['note']
            profile.save(update_fields=['xp', 'updated_at'])
        return Response({'success': True, 'data': {'body': note.body, 'xp': profile.xp}})


class ActivityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        kind = request.data.get('kind')
        action_key = str(request.data.get('action_key', '')).strip()
        language_slug = request.data.get('language_slug')
        if kind not in XP_BY_ACTIVITY or not action_key:
            return Response({'success': False, 'error': {'message': 'Invalid learning activity.'}, 'data': None}, status=status.HTTP_400_BAD_REQUEST)
        language = Language.objects.filter(slug=language_slug, status='active').first() if language_slug else None
        profile = profile_for(request.user)
        with transaction.atomic():
            activity, created = LearningActivity.objects.get_or_create(
                user=request.user, kind=kind, action_key=action_key,
                defaults={'language': language, 'xp_awarded': XP_BY_ACTIVITY[kind]},
            )
            if created:
                profile.xp += activity.xp_awarded
            if kind == 'daily_challenge' and created:
                today = timezone.localdate()
                if profile.last_activity_date == today - timedelta(days=1):
                    profile.current_streak += 1
                elif profile.last_activity_date != today:
                    profile.current_streak = 1
                profile.last_activity_date = today
            profile.save()
        return Response({'success': True, 'data': {'awarded_xp': activity.xp_awarded if created else 0, 'xp': profile.xp, 'streak': profile.current_streak}})


class LastLanguageView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        language = get_object_or_404(Language, slug=request.data.get('language_slug'), status='active')
        profile = profile_for(request.user)
        profile.last_language = language
        profile.save(update_fields=['last_language', 'updated_at'])
        return Response({'success': True, 'data': {'last_language_slug': language.slug}})
