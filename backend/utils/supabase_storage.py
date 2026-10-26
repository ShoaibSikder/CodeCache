"""Django file storage backed by the configured Supabase Storage bucket."""

import mimetypes
import posixpath

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible
from .supabase_client import get_supabase_storage


@deconstructible
class SupabaseStorage(Storage):
    def _bucket(self):
        if not settings.SUPABASE_URL or not settings.SUPABASE_SERVICE_KEY:
            raise RuntimeError('Set SUPABASE_URL and SUPABASE_SERVICE_KEY to enable file uploads.')
        storage = get_supabase_storage()
        if storage is None:
            raise RuntimeError('Could not initialize Supabase Storage.')
        return storage.from_(settings.SUPABASE_BUCKET)

    def _clean_name(self, name):
        normalized = posixpath.normpath(name.replace('\\', '/')).lstrip('/')
        if normalized in ('', '.') or normalized == '..' or normalized.startswith('../'):
            raise ValueError('Invalid Supabase storage path.')
        return normalized

    def _open(self, name, mode='rb'):
        if mode not in ('rb', 'r'):
            raise ValueError('Supabase storage supports read-only file access.')
        data = self._bucket().download(self._clean_name(name))
        return ContentFile(data, name=name)

    def _save(self, name, content):
        name = self._clean_name(name)
        if hasattr(content, 'chunks'):
            data = b''.join(content.chunks())
        else:
            data = content.read()
        content_type = getattr(content, 'content_type', None) or mimetypes.guess_type(name)[0] or 'application/octet-stream'
        self._bucket().upload(
            path=name,
            file=data,
            file_options={'content-type': content_type, 'upsert': 'false'},
        )
        return name

    def delete(self, name):
        if name:
            self._bucket().remove([self._clean_name(name)])

    def exists(self, name):
        name = self._clean_name(name)
        directory, filename = posixpath.split(name)
        return any(item.get('name') == filename for item in self._bucket().list(directory or ''))

    def url(self, name):
        return self._bucket().get_public_url(self._clean_name(name))

    def size(self, name):
        name = self._clean_name(name)
        directory, filename = posixpath.split(name)
        for item in self._bucket().list(directory or ''):
            if item.get('name') == filename and item.get('metadata'):
                return item['metadata'].get('size')
        raise FileNotFoundError(name)

    def get_available_name(self, name, max_length=None):
        name = self._clean_name(name)
        return super().get_available_name(name, max_length)
