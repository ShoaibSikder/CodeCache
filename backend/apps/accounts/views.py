"""
Views for the accounts app.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView as BaseTokenRefreshView
from django.contrib.auth import get_user_model
from apps.common.constants import UserRole
from apps.common.permissions import IsSuperAdmin

from .serializers import (
    UserSerializer,
    UserProfileSerializer,
    UserCreateSerializer,
    LoginSerializer,
    PasswordChangeSerializer,
)

User = get_user_model()


class RegisterView(APIView):
    """
    POST /api/v1/auth/register/
    Register a new user account.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Registration failed.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    POST /api/v1/auth/login/
    Authenticate user and return JWT tokens.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            return Response({
                'success': True,
                'data': {
                    'user': UserSerializer(user).data,
                    'tokens': {
                        'access': str(refresh.access_token),
                        'refresh': str(refresh),
                    }
                }
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Login failed.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class TokenRefreshView(BaseTokenRefreshView):
    """
    POST /api/v1/auth/refresh/
    Refresh access token using refresh token.
    """

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'success': True,
                'data': {
                    'access': serializer.validated_data['access'],
                }
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_401_UNAUTHORIZED,
                'message': 'Token refresh failed.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_401_UNAUTHORIZED)


class ProfileView(APIView):
    """
    GET /api/v1/auth/profile/
    Get the authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response({
            'success': True,
            'data': serializer.data
        })

    def patch(self, request):
        """Update user profile."""
        serializer = UserProfileSerializer(
            request.user,
            data=request.data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'data': serializer.data
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Profile update failed.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class PasswordChangeView(APIView):
    """
    POST /api/v1/auth/password-change/
    Change the authenticated user's password.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = PasswordChangeSerializer(
            data=request.data,
            context={'request': request}
        )
        if serializer.is_valid():
            user = request.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({
                'success': True,
                'data': {
                    'message': 'Password changed successfully.'
                }
            })
        return Response({
            'success': False,
            'error': {
                'code': status.HTTP_400_BAD_REQUEST,
                'message': 'Password change failed.',
                'details': serializer.errors
            },
            'data': None
        }, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/
    Blacklist the refresh token to log out.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'success': True,
                'data': {
                    'message': 'Logged out successfully.'
                }
            })
        except Exception as e:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_400_BAD_REQUEST,
                    'message': 'Logout failed.',
                    'details': str(e)
                },
                'data': None
            }, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):
    """
    GET /api/v1/auth/users/
    List all users (Admin only).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_admin:
            return Response({
                'success': False,
                'error': {
                    'code': status.HTTP_403_FORBIDDEN,
                    'message': 'You do not have permission to view users.'
                },
                'data': None
            }, status=status.HTTP_403_FORBIDDEN)

        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({
            'success': True,
            'data': serializer.data
        })


class AdminUserDetailView(APIView):
    """Allow super-admins to change account roles and activation status."""
    permission_classes = [IsAuthenticated, IsSuperAdmin]

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                'success': False,
                'error': {'code': status.HTTP_404_NOT_FOUND, 'message': 'User not found.'},
                'data': None,
            }, status=status.HTTP_404_NOT_FOUND)

        changes = {}
        if 'role' in request.data:
            role = request.data['role']
            valid_roles = {value for value, _label in UserRole.CHOICES}
            if role not in valid_roles:
                return Response({
                    'success': False,
                    'error': {'code': status.HTTP_400_BAD_REQUEST, 'message': 'Invalid user role.'},
                    'data': None,
                }, status=status.HTTP_400_BAD_REQUEST)
            changes['role'] = role

        if 'is_active' in request.data:
            is_active = request.data['is_active']
            if not isinstance(is_active, bool):
                return Response({
                    'success': False,
                    'error': {'code': status.HTTP_400_BAD_REQUEST, 'message': 'is_active must be a boolean.'},
                    'data': None,
                }, status=status.HTTP_400_BAD_REQUEST)
            changes['is_active'] = is_active

        if not changes:
            return Response({
                'success': False,
                'error': {'code': status.HTTP_400_BAD_REQUEST, 'message': 'Provide a role or is_active update.'},
                'data': None,
            }, status=status.HTTP_400_BAD_REQUEST)

        if user.pk == request.user.pk and (
            changes.get('is_active') is False
            or changes.get('role', user.role) != user.role
        ):
            return Response({
                'success': False,
                'error': {'code': status.HTTP_400_BAD_REQUEST, 'message': 'You cannot change your own role or deactivate your account.'},
                'data': None,
            }, status=status.HTTP_400_BAD_REQUEST)

        for key, value in changes.items():
            setattr(user, key, value)
        if 'role' in changes:
            user.is_staff = changes['role'] in (UserRole.ADMIN, UserRole.SUPER_ADMIN)
            user.is_superuser = changes['role'] == UserRole.SUPER_ADMIN
        update_fields = list(changes)
        if 'role' in changes:
            update_fields.extend(['is_staff', 'is_superuser'])
        user.save(update_fields=update_fields)
        return Response({'success': True, 'data': UserSerializer(user).data})
