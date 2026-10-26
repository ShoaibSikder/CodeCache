from types import SimpleNamespace
from unittest.mock import patch

from django.test import SimpleTestCase, override_settings
from rest_framework.test import APIRequestFactory

from .views import RunCodeView, SupportedLanguagesView


class PlaygroundViewTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.execution = SimpleNamespace(
            status='submitted', output='', error='', execution_time=None,
            memory_used=None, save=lambda: None,
        )

    @override_settings(JDOODLE_SETTINGS={
        'API_URL': 'https://api.jdoodle.example/v1/execute',
        'CLIENT_ID': 'test-id',
        'CLIENT_SECRET': 'test-secret',
        'VERSION_INDEX': '0',
    })
    @patch('apps.playground.views.requests.post')
    @patch('apps.playground.views.CodeExecution.objects.create')
    def test_runs_python_with_jdoodle_and_returns_normalized_output(self, create, post):
        create.return_value = self.execution
        post.return_value.status_code = 200
        post.return_value.json.return_value = {
            'output': 'Hello from CodeCache!\n',
            'statusCode': 200,
            'memory': '7768',
            'cpuTime': '0.02',
        }

        request = self.factory.post('/api/v1/playground/run/', {
            'language': 'python', 'code': 'print("Hello from CodeCache!")', 'stdin': '',
        }, format='json')
        response = RunCodeView.as_view()(request)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['data']['output'], 'Hello from CodeCache!\n')
        self.assertEqual(response.data['data']['execution_time'], '0.02')
        self.assertEqual(response.data['data']['memory_used'], '7768')
        payload = post.call_args.kwargs['json']
        self.assertEqual(payload['language'], 'python3')
        self.assertEqual(payload['stdin'], '')
        self.assertEqual(payload['clientSecret'], 'test-secret')
        self.assertNotIn('clientSecret', response.data)

    @override_settings(JDOODLE_SETTINGS={
        'API_URL': 'https://api.jdoodle.example/v1/execute',
        'CLIENT_ID': '',
        'CLIENT_SECRET': '',
        'VERSION_INDEX': '0',
    })
    @patch('apps.playground.views.CodeExecution.objects.create')
    def test_missing_credentials_returns_configuration_error(self, create):
        response = RunCodeView.as_view()(self.factory.post(
            '/api/v1/playground/run/', {'language': 'python', 'code': 'print(1)'}, format='json',
        ))

        self.assertEqual(response.status_code, 503)
        self.assertIn('JDoodle is not configured', response.data['error']['message'])
        create.assert_not_called()

    @override_settings(JDOODLE_SETTINGS={
        'API_URL': 'https://api.jdoodle.example/v1/execute',
        'CLIENT_ID': 'test-id',
        'CLIENT_SECRET': 'test-secret',
        'VERSION_INDEX': '0',
    })
    @patch('apps.playground.views.requests.post')
    @patch('apps.playground.views.CodeExecution.objects.create')
    def test_quota_error_is_reported_without_provider_secrets(self, create, post):
        create.return_value = self.execution
        post.return_value.status_code = 429
        post.return_value.json.return_value = {'error': 'quota exceeded'}

        response = RunCodeView.as_view()(self.factory.post(
            '/api/v1/playground/run/', {'language': 'python', 'code': 'print(1)'}, format='json',
        ))

        self.assertEqual(response.status_code, 429)
        self.assertIn('credits or rate limit', response.data['error']['message'])
        self.assertNotIn('test-secret', str(response.data))

    def test_supported_languages_are_jdoodle_canonical_aliases(self):
        response = SupportedLanguagesView.as_view()(self.factory.get('/api/v1/playground/languages/'))
        names = {item['name'] for item in response.data['data']}

        self.assertIn('python', names)
        self.assertIn('javascript', names)
        self.assertIn('cpp', names)
