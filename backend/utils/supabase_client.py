"""
Supabase client for CodeCache.
Handles storage bucket operations for media files.
Images are stored as: language_name/section_name/subsection_name/filename
"""

from django.conf import settings
from supabase import create_client, Client

_supabase_client = None


def get_supabase() -> Client:
    """Get or create the Supabase client singleton."""
    global _supabase_client
    if _supabase_client is None:
        url = settings.SUPABASE_URL
        key = settings.SUPABASE_SERVICE_KEY
        if url and key:
            _supabase_client = create_client(url, key)
    return _supabase_client


def get_supabase_storage():
    """Get the Supabase storage client."""
    supabase = get_supabase()
    if supabase:
        return supabase.storage
    return None


