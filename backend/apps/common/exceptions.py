"""
Custom exception handler for CodeCache.
"""

from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler that returns consistent error responses.
    """
    response = exception_handler(exc, context)

    if response is not None:
        error_data = {
            'success': False,
            'error': {
                'code': response.status_code,
                'message': get_error_message(response.data),
                'details': response.data if isinstance(response.data, dict) else None,
            },
            'data': None,
        }
        response.data = error_data

    return response


def get_error_message(data):
    """
    Extract a human-readable error message from response data.
    """
    if isinstance(data, str):
        return data
    if isinstance(data, list):
        return data[0] if data else 'An error occurred.'
    if isinstance(data, dict):
        if 'detail' in data:
            return data['detail']
        if 'non_field_errors' in data:
            return data['non_field_errors'][0]
        for key, value in data.items():
            if isinstance(value, list):
                return f"{key}: {value[0]}"
            return f"{key}: {value}"
    return 'An error occurred.'


class CodeCacheAPIException(APIException):
    """
    Base API exception for CodeCache.
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'An error occurred.'
    default_code = 'error'

    def __init__(self, detail=None, code=None, status_code=None):
        if status_code is not None:
            self.status_code = status_code
        super().__init__(detail, code)


class NotFoundException(CodeCacheAPIException):
    """Resource not found."""
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Resource not found.'
    default_code = 'not_found'


class ConflictException(CodeCacheAPIException):
    """Resource conflict (e.g., duplicate slug)."""
    status_code = status.HTTP_409_CONFLICT
    default_detail = 'Resource conflict.'
    default_code = 'conflict'


class ValidationException(CodeCacheAPIException):
    """Validation error."""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    default_detail = 'Validation failed.'
    default_code = 'validation_error'
