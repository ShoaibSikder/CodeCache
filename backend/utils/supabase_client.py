"""
Supabase client for CodeCache.
Handles storage bucket operations for media files.
Images are stored as: language_name/section_name/subsection_name/filename
"""

import os
import uuid
from supabase import create_client, Client

_supabase_client = None


def get_supabase() -> Client:
    """Get or create the Supabase client singleton."""
    global _supabase_client
    if _supabase_client is None:
        url = os.getenv('SUPABASE_URL', '')
        key = os.getenv('SUPABASE_SERVICE_KEY', '')
        if url and key:
            _supabase_client = create_client(url, key)
    return _supabase_client


def get_supabase_storage():
    """Get the Supabase storage client."""
    supabase = get_supabase()
    if supabase:
        return supabase.storage
    return None


def generate_storage_path(language_name, section_name, subsection_name, filename):
    """
    Generate a storage path following the pattern:
    language_name/section_name/subsection_name/filename
    """
    # Sanitize names for path safety
    safe_lang = _sanitize_path(language_name)
    safe_section = _sanitize_path(section_name) if section_name else 'general'
    safe_subsection = _sanitize_path(subsection_name) if subsection_name else 'general'
    
    # Generate unique filename
    ext = filename.split('.')[-1] if '.' in filename else ''
    unique_name = f"{uuid.uuid4().hex[:8]}.{ext}" if ext else f"{uuid.uuid4().hex[:8]}"
    
    return f"{safe_lang}/{safe_section}/{safe_subsection}/{unique_name}"


def _sanitize_path(name):
    """Sanitize a name for use in a path."""
    return name.lower().replace(' ', '-').replace('_', '-').replace('/', '-')


async def upload_image(file_data, language_name, section_name='', subsection_name='', filename='image.png'):
    """
    Upload an image to Supabase Storage.
    Returns the public URL of the uploaded file.
    """
    storage = get_supabase_storage()
    if not storage:
        raise RuntimeError('Supabase storage is not configured')
    
    bucket_name = os.getenv('SUPABASE_BUCKET', 'codecache-media')
    path = generate_storage_path(language_name, section_name, subsection_name, filename)
    
    # Upload file
    result = storage.from_(bucket_name).upload(
        path=path,
        file=file_data,
        file_options={'content-type': f'image/{filename.split(".")[-1]}'}
    )
    
    # Get public URL
    supabase_url = os.getenv('SUPABASE_URL', '')
    public_url = f"{supabase_url}/storage/v1/object/public/{bucket_name}/{path}"
    
    return {
        'path': path,
        'url': public_url
    }


async def delete_image(path):
    """Delete an image from Supabase Storage."""
    storage = get_supabase_storage()
    if not storage:
        raise RuntimeError('Supabase storage is not configured')
    
    bucket_name = os.getenv('SUPABASE_BUCKET', 'codecache-media')
    result = storage.from_(bucket_name).remove([path])
    return result


def get_image_url(path):
    """Get the public URL for an image path."""
    supabase_url = os.getenv('SUPABASE_URL', '')
    bucket_name = os.getenv('SUPABASE_BUCKET', 'codecache-media')
    return f"{supabase_url}/storage/v1/object/public/{bucket_name}/{path}"
