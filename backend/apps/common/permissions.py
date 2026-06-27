"""
Custom permissions for CodeCache.
"""

from rest_framework import permissions
from .constants import UserRole, PERMISSION_MATRIX, PermissionAction


class IsSuperAdmin(permissions.BasePermission):
    """Only Super Admin can access."""

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role == UserRole.SUPER_ADMIN
        )


class IsAdmin(permissions.BasePermission):
    """Admin and Super Admin can access."""

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]
        )


class IsEditor(permissions.BasePermission):
    """Editor, Admin, and Super Admin can access."""

    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [
                UserRole.SUPER_ADMIN,
                UserRole.ADMIN,
                UserRole.EDITOR
            ]
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Admin can perform any action.
    Anyone can read (GET, HEAD, OPTIONS).
    """

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return (
            request.user and
            request.user.is_authenticated and
            request.user.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]
        )


class HasRolePermission(permissions.BasePermission):
    """
    Generic permission that checks if the user has a specific permission.
    Usage: permission_classes = [HasRolePermission]
    Set `required_permission` attribute on the view.
    """

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        required_permission = getattr(view, 'required_permission', None)
        if not required_permission:
            return True

        user_permissions = PERMISSION_MATRIX.get(request.user.role, [])
        return required_permission in user_permissions


class ReadOnly(permissions.BasePermission):
    """Allow read-only access to anyone."""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS
