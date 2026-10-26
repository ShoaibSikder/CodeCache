"""Code playground backed by the JDoodle Compiler API."""

import requests

from django.conf import settings
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CodeExecution


JDOODLE_LANGUAGES = {
    'python': 'python3',
    'javascript': 'nodejs',
    'java': 'java',
    'cpp': 'cpp',
    'c': 'c',
    'csharp': 'csharp',
    'go': 'go',
    'ruby': 'ruby',
    'rust': 'rust',
    'php': 'php',
    'swift': 'swift',
    'kotlin': 'kotlin',
    'typescript': 'typescript',
    'sql': 'sql',
}
LANGUAGE_ALIASES = {'python3': 'python', 'js': 'javascript', 'ts': 'typescript'}
MAX_CODE_LENGTH = 40_000
MAX_STDIN_LENGTH = 10_000


def jdoodle_failure_message(http_status, provider_error=''):
    if http_status == 401 or http_status == 403:
        return 'JDoodle rejected the credentials. Check JDOODLE_CLIENT_ID and JDOODLE_CLIENT_SECRET.'
    if http_status == 429:
        return 'JDoodle daily execution credits or rate limit have been reached.'
    if http_status and http_status >= 500:
        return 'JDoodle is temporarily unavailable. Try again shortly.'
    if provider_error:
        return str(provider_error)[:300]
    return 'JDoodle could not execute this request. Check the language and API configuration.'


class RunCodeView(APIView):
    """POST /api/v1/playground/run/"""
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        language = str(data.get('language', '')).lower().strip()
        language = LANGUAGE_ALIASES.get(language, language)
        code = data.get('code', data.get('script', ''))
        stdin = data.get('stdin', '')

        if not isinstance(code, str) or not code.strip():
            return Response({'success': False, 'error': {'code': 400, 'message': 'Code is required.'}, 'data': None}, status=400)
        if len(code) > MAX_CODE_LENGTH or not isinstance(stdin, str) or len(stdin) > MAX_STDIN_LENGTH:
            return Response({'success': False, 'error': {'code': 400, 'message': 'Code or standard input exceeds the allowed size.'}, 'data': None}, status=400)
        jdoodle_language = JDOODLE_LANGUAGES.get(language)
        if not jdoodle_language:
            return Response({'success': False, 'error': {'code': 400, 'message': f'Unsupported language: {language}.'}, 'data': None}, status=400)

        config = settings.JDOODLE_SETTINGS
        client_id = config['CLIENT_ID']
        client_secret = config['CLIENT_SECRET']
        if not client_id or not client_secret:
            return Response({
                'success': False,
                'error': {'code': 503, 'message': 'JDoodle is not configured. Add its client ID and secret to backend/.env.'},
                'data': None,
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

        execution = CodeExecution.objects.create(language=language, code=code, status='submitted')
        payload = {
            'clientId': client_id,
            'clientSecret': client_secret,
            'script': code,
            'language': jdoodle_language,
            'versionIndex': str(config['VERSION_INDEX']),
            'stdin': stdin,
        }

        try:
            response = requests.post(config['API_URL'], json=payload, timeout=30)
            try:
                result = response.json()
            except ValueError:
                result = {}

            provider_error = result.get('error') if isinstance(result, dict) else ''
            if response.status_code != 200 or provider_error:
                message = jdoodle_failure_message(response.status_code, provider_error)
                execution.status = 'failed'
                execution.error = message
                execution.save()
                error_code = status.HTTP_429_TOO_MANY_REQUESTS if response.status_code == 429 else status.HTTP_502_BAD_GATEWAY
                return Response({'success': False, 'error': {'code': error_code, 'message': message}, 'data': None}, status=error_code)

            output = result.get('output', '')
            execution.status = 'completed'
            execution.output = output
            execution.execution_time = _as_float(result.get('cpuTime'))
            execution.memory_used = _as_int(result.get('memory'))
            execution.save()
            return Response({
                'success': True,
                'data': {
                    'output': output,
                    'error': '',
                    'execution_time': result.get('cpuTime'),
                    'memory_used': result.get('memory'),
                    'status': 'Completed',
                    'exit_code': result.get('statusCode'),
                },
            })
        except requests.RequestException:
            execution.status = 'failed'
            execution.error = 'Could not reach JDoodle.'
            execution.save()
            return Response({
                'success': False,
                'error': {'code': 502, 'message': 'Could not reach JDoodle. Check the backend network connection and try again.'},
                'data': None,
            }, status=status.HTTP_502_BAD_GATEWAY)


def _as_float(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _as_int(value):
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


class SupportedLanguagesView(APIView):
    """GET /api/v1/playground/languages/"""
    permission_classes = [AllowAny]

    def get(self, request):
        return Response({
            'success': True,
            'data': [{'id': name, 'name': name} for name in JDOODLE_LANGUAGES],
        })
