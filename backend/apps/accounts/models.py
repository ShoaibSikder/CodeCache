"""
Custom User model for CodeCache with role-based access control.
"""

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.common.models import BaseModel
from apps.common.constants import UserRole
from apps.common.validators import validate_username


class UserManager(BaseUserManager):
    """Custom user manager for the User model."""

    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', UserRole.SUPER_ADMIN)

        if not extra_fields.get('is_staff'):
            raise ValueError('Superuser must have is_staff=True.')
        if not extra_fields.get('is_superuser'):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    """
    Custom User model with UUID primary key and role-based access.
    """
    username = models.CharField(
        max_length=50,
        unique=True,
        validators=[validate_username],
        help_text="Unique username for login"
    )
    email = models.EmailField(
        unique=True,
        help_text="Email address"
    )
    first_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="First name"
    )
    last_name = models.CharField(
        max_length=50,
        blank=True,
        help_text="Last name"
    )
    role = models.CharField(
        max_length=20,
        choices=UserRole.CHOICES,
        default=UserRole.USER,
        db_index=True,
        help_text="User role for access control"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the user account is active"
    )
    is_staff = models.BooleanField(
        default=False,
        help_text="Whether the user can access the admin site"
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        db_table = 'accounts_user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.email})"

    @property
    def full_name(self):
        """Return the user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    @property
    def is_super_admin(self):
        """Check if user is a super admin."""
        return self.role == UserRole.SUPER_ADMIN

    @property
    def is_admin(self):
        """Check if user is an admin or super admin."""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN]

    @property
    def is_editor(self):
        """Check if user is an editor, admin, or super admin."""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.ADMIN, UserRole.EDITOR]

    def has_permission(self, permission_action):
        """
        Check if the user has a specific permission.
        """
        from apps.common.constants import PERMISSION_MATRIX
        user_permissions = PERMISSION_MATRIX.get(self.role, [])
        return permission_action in user_permissions
