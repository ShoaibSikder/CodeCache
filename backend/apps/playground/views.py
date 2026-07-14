"""
Playground views for CodeCache - Judge0 integration.
"""

import os
import requests
import base64

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import CodeExecution, SupportedLanguage


# Judge0 language mapping
JUDGE0_LANGUAGES = {
    'python': 71,      # Python 3.8
    'python3': 71,
    'javascript': 63,  # Node.js
    'js': 63,
    'java': 62,        # Java 13
    'cpp': 54,         # C++ GCC 9.2.0
    'c': 50,           # C GCC 9.2.0
    'csharp': 51,      # C# Mono
    'go': 60,          # Go 1.13.3
    'ruby': 72,        # Ruby 2.7.0
    'rust': 73,        # Rust 1.40.0
    'php': 68,         # PHP 7.4.1
    'swift': 83,       # Swift 5.1
    'kotlin': 78,      # Kotlin 1.3.70
    'typescript': 74,  # TypeScript 3.7.4
    'ts': 74,
    'sql': 82,         # SQLite 3.27.2
}


class RunCodeView(APIView):
    """
    POST /api/v1/playground/run/
    Execute code using Judge0 API.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        data = request.data
        language = data.get('language', '').lower().strip()
        code = data.get('code', '')
        stdin = data.get('stdin', '')

        if not language:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Language is required.'
                },
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        if not code:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Code is required.'
                },
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get Judge0 language ID
        judge0_lang_id = JUDGE0_LANGUAGES.get(language)
        if not judge0_lang_id:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': f'Unsupported language: {language}. Supported: {", ".join(JUDGE0_LANGUAGES.keys())}'
                },
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)

        # Get Judge0 API credentials from settings
        judge0_url = os.getenv('JUDGE0_API_URL', 'https://judge0-ce.p.rapidapi.com')
        api_key = os.getenv('JUDGE0_API_KEY', '')
        api_host = os.getenv('JUDGE0_API_HOST', 'judge0-ce.p.rapidapi.com')

        # Prepare the submission
        encoded_code = base64.b64encode(code.encode('utf-8')).decode('utf-8')
        encoded_stdin = base64.b64encode(stdin.encode('utf-8')).decode('utf-8') if stdin else None

        submission_data = {
            'language_id': judge0_lang_id,
            'source_code': encoded_code,
            'stdin': encoded_stdin or '',
        }

        # Create execution record
        execution = CodeExecution.objects.create(
            language=language,
            code=code,
            status='submitted'
        )

        # Headers for Judge0 API
        headers = {
            'content-type': 'application/json',
        }

        if api_key:
            headers['X-RapidAPI-Key'] = api_key
        if api_host:
            headers['X-RapidAPI-Host'] = api_host

        try:
            # Submit code to Judge0
            submit_url = f"{judge0_url}/submissions"
            submit_response = requests.post(
                submit_url,
                json=submission_data,
                headers=headers,
                params={'base64_encoded': 'true', 'wait': 'true'},
                timeout=30
            )

            if submit_response.status_code != 201:
                execution.status = 'failed'
                execution.error = f"Judge0 submission failed: {submit_response.text}"
                execution.save()
                return Response({
                    'success': False,
                    'error': {
                        'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                        'message': 'Code execution service unavailable.',
                        'details': submit_response.text
                    },
                    'data': None
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            result = submit_response.json()

            # Decode the output
            output = ''
            error_output = ''
            compile_output = ''

            if result.get('stdout'):
                output = base64.b64decode(result['stdout']).decode('utf-8', errors='replace')
            if result.get('stderr'):
                error_output = base64.b64decode(result['stderr']).decode('utf-8', errors='replace')
            if result.get('compile_output'):
                compile_output = base64.b64decode(result['compile_output']).decode('utf-8', errors='replace')

            # Update execution record
            execution.status = result.get('status', {}).get('description', 'completed').lower()
            execution.output = output
            execution.error = error_output or compile_output
            execution.execution_time = result.get('time')
            execution.memory_used = result.get('memory')
            execution.judge0_token = result.get('token', '')
            execution.save()

            return Response({
                'success': True,
                'data': {
                    'output': output,
                    'error': error_output or compile_output,
                    'execution_time': result.get('time'),
                    'memory_used': result.get('memory'),
                    'status': result.get('status', {}).get('description', 'Completed'),
                }
            })

        except requests.RequestException as e:
            execution.status = 'failed'
            execution.error = str(e)
            execution.save()
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Failed to execute code.',
                    'details': str(e)
                },
                'data': None
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SupportedLanguagesView(APIView):
    """
    GET /api/v1/playground/languages/
    Get list of supported playground languages.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        languages = [
            {'id': lang_id, 'name': name}
            for name, lang_id in JUDGE0_LANGUAGES.items()
        ]

        # Remove duplicates (e.g., 'python' and 'python3')
        seen = set()
        unique_languages = []
        for lang in languages:
            if lang['id'] not in seen:
                seen.add(lang['id'])
                unique_languages.append(lang)

        return Response({
            'success': True,
            'data': unique_languages
        })


class ExecutionStatusView(APIView):
    """
    GET /api/v1/playground/status/{token}/
    Get the status of a code execution.
    """
    permission_classes = [AllowAny]

    def get(self, request, token):
        try:
            execution = CodeExecution.objects.get(judge0_token=token)
        except CodeExecution.DoesNotExist:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_404_NOT_FOUND,
                    'message': 'Execution not found.'
                },
                'data': None
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            'success': True,
            'data': {
                'id': str(execution.id),
                'language': execution.language,
                'status': execution.status,
                'output': execution.output,
                'error': execution.error,
                'execution_time': execution.execution_time,
                'memory_used': execution.memory_used,
                'created_at': execution.created_at.isoformat(),
            }
        })
