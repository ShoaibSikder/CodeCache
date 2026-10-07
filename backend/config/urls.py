"""
URL configuration for CodeCache project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from groq import Groq


def health_check(request):
    return JsonResponse({"service": "CodeCache API", "status": "ok"})


def warmup(request):
    return JsonResponse({"status": "warm"})


@csrf_exempt
def ai_code_doctor(request):
    """
    POST /api/v1/ai/code-doctor/
    AI-powered code analysis using Groq API.
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': {'code': 405, 'message': 'Method not allowed. Use POST.'},
            'data': None
        }, status=405)

    try:
        body = json.loads(request.body)
        code = body.get('code', '').strip()
        language = body.get('language', 'javascript')

        if not code:
            return JsonResponse({
                'success': False,
                'error': {'code': 400, 'message': 'Code is required.'},
                'data': None
            }, status=400)

        groq_api_key = os.getenv('GROQ_API_KEY', '')
        if not groq_api_key:
            return JsonResponse({
                'success': False,
                'error': {'code': 500, 'message': 'AI service is not configured.'},
                'data': None
            }, status=500)

        client = Groq(api_key=groq_api_key)

        system_prompt = (
            "You are CodeCache AI Code Doctor, an expert programming assistant. "
            "Analyze the provided code and:\n"
            "1. Identify any bugs, errors, or issues\n"
            "2. Explain what's wrong and why\n"
            "3. Provide a corrected version of the code\n"
            "4. Add helpful tips or best practices related to the code\n"
            "5. If the code is already correct, suggest optimizations or improvements\n"
            "Be concise but thorough. Format your response clearly."
        )

        user_prompt = f"Language: {language}\n\nCode:\n```\n{code}\n```\n\nPlease analyze this code."

        completion = client.chat.completions.create(
            model=os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile'),
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt}
            ],
            temperature=0.3,
            max_tokens=2048,
        )

        result = completion.choices[0].message.content

        return JsonResponse({
            'success': True,
            'data': {
                'result': result,
                'language': language,
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': {'code': 400, 'message': 'Invalid JSON body.'},
            'data': None
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': {'code': 500, 'message': 'AI analysis failed.', 'details': str(e)},
            'data': None
        }, status=500)


@csrf_exempt
def ai_generate_quiz(request):
    """
    POST /api/v1/ai/generate-quiz/
    Generate multiple-choice quiz questions using Groq API.
    """
    if request.method != 'POST':
        return JsonResponse({
            'success': False,
            'error': {'code': 405, 'message': 'Method not allowed. Use POST.'},
            'data': None
        }, status=405)

    try:
        body = json.loads(request.body)
        language = body.get('language', 'programming').strip() or 'programming'
        topic = body.get('topic', '').strip()

        groq_api_key = os.getenv('GROQ_API_KEY', '')
        if not groq_api_key:
            return JsonResponse({
                'success': False,
                'error': {'code': 500, 'message': 'AI service is not configured.'},
                'data': None
            }, status=500)

        client = Groq(api_key=groq_api_key)
        topic_text = f" Topic focus: {topic}." if topic else ""
        prompt = (
            f"Generate 4 beginner-friendly multiple-choice quiz questions for {language}."
            f"{topic_text} Return only valid JSON with this shape: "
            '{"questions":[{"question":"...","options":["...","...","...","..."],'
            '"correctIndex":0,"explanation":"..."}]}. '
            "Use exactly four options per question. correctIndex must be 0, 1, 2, or 3."
        )

        completion = client.chat.completions.create(
            model=os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile'),
            messages=[
                {'role': 'system', 'content': 'You generate concise valid JSON only.'},
                {'role': 'user', 'content': prompt}
            ],
            temperature=0.5,
            max_tokens=1600,
            response_format={'type': 'json_object'},
        )

        content = completion.choices[0].message.content
        payload = json.loads(content)
        questions = payload.get('questions', [])

        return JsonResponse({
            'success': True,
            'data': {
                'questions': questions,
                'language': language,
            }
        })

    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': {'code': 400, 'message': 'Invalid JSON body or AI response.'},
            'data': None
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': {'code': 500, 'message': 'AI quiz generation failed.', 'details': str(e)},
            'data': None
        }, status=500)


urlpatterns = [
    path('', health_check),
    path('warmup/', warmup),
    path('admin/', admin.site.urls),
    path('api/v1/auth/', include('apps.accounts.urls')),
    path('api/v1/languages/', include('apps.languages.urls')),
    path('api/v1/admin/languages/', include('apps.languages.admin_urls')),
    path('api/v1/admin/sections/', include('apps.content.section_urls')),
    path('api/v1/admin/subsections/', include('apps.content.subsection_urls')),
    path('api/v1/admin/content-items/', include('apps.content.contentitem_urls')),
    path('api/v1/search/', include('apps.search.urls')),
    path('api/v1/analytics/', include('apps.analytics.urls')),
    path('api/v1/playground/', include('apps.playground.urls')),
    path('api/v1/learning/', include('apps.learning.urls')),
    path('api/v1/ai/code-doctor/', ai_code_doctor, name='ai-code-doctor'),
    path('api/v1/ai/generate-quiz/', ai_generate_quiz, name='ai-generate-quiz'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
