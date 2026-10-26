from types import SimpleNamespace
from unittest.mock import patch

from django.core.files.base import ContentFile
from django.test import SimpleTestCase, override_settings

from utils.supabase_storage import SupabaseStorage


@override_settings(
    SUPABASE_URL='https://project.supabase.co',
    SUPABASE_SERVICE_KEY='test-service-key',
    SUPABASE_BUCKET='codecache-assets',
)
class SupabaseStorageTests(SimpleTestCase):
    def setUp(self):
        self.bucket = SimpleNamespace(
            upload=lambda **kwargs: {'path': kwargs['path']},
            download=lambda path: b'image-bytes',
            remove=lambda paths: paths,
            get_public_url=lambda path: f'https://project.supabase.co/storage/v1/object/public/codecache-assets/{path}',
            list=lambda path: [],
        )
        self.storage_client = SimpleNamespace(from_=lambda bucket: self.bucket)
        self.storage = SupabaseStorage()

    @patch('utils.supabase_storage.get_supabase_storage')
    def test_save_uses_bucket_and_returns_storage_path(self, get_storage):
        get_storage.return_value = self.storage_client

        saved_name = self.storage._save('languages/icons/python.png', ContentFile(b'image-bytes', name='python.png'))

        self.assertEqual(saved_name, 'languages/icons/python.png')
        get_storage.assert_called_once_with()

    @patch('utils.supabase_storage.get_supabase_storage')
    def test_public_url_download_and_delete_use_bucket_objects(self, get_storage):
        get_storage.return_value = self.storage_client

        self.assertTrue(self.storage.url('languages/icons/python.png').endswith('/languages/icons/python.png'))
        self.assertEqual(self.storage._open('languages/icons/python.png').read(), b'image-bytes')
        self.storage.delete('languages/icons/python.png')

    @override_settings(SUPABASE_SERVICE_KEY='')
    def test_missing_storage_credentials_fail_clearly(self):
        with self.assertRaisesMessage(RuntimeError, 'SUPABASE_URL and SUPABASE_SERVICE_KEY'):
            self.storage._bucket()
