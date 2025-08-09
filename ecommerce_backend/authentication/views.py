"""
Authentication Views for ALX Project Nexus E-commerce Backend

This module provides API endpoints for user authentication and management.
Includes registration, login, profile management, and JWT token handling.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import update_last_login
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse
from drf_spectacular.openapi import OpenApiTypes

from .serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    UserUpdateSerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer,
    PasswordResetSerializer,
    UserLoginSerializer
)

User = get_user_model()
logger = logging.getLogger(__name__)


class UserRegistrationView(generics.CreateAPIView):
    """
    User registration endpoint.
    
    Allows new users to create an account with email and password.
    Returns user data and JWT tokens upon successful registration.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]
    
    @extend_schema(
        summary='User Registration',
        description='''
        Register a new user account with email and password.
        
        **Note**: This endpoint is public and doesn't require authentication.
        
        Upon successful registration, the response will include:
        - User profile information
        - JWT access token (valid for 1 hour)
        - JWT refresh token (valid for 7 days)
        ''',
        examples=[
            OpenApiExample(
                'Registration Example',
                value={
                    'email': 'newuser@example.com',
                    'password': 'SecurePassword123!',
                    'password_confirm': 'SecurePassword123!',
                    'first_name': 'John',
                    'last_name': 'Doe'
                },
                request_only=True,
            ),
        ],
        responses={
            201: OpenApiResponse(
                description='User registered successfully',
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            'user': {
                                'id': 1,
                                'email': 'newuser@example.com',
                                'first_name': 'John',
                                'last_name': 'Doe',
                                'date_joined': '2025-08-09T10:30:00Z'
                            },
                            'tokens': {
                                'access': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...',
                                'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...'
                            },
                            'message': 'User registered successfully'
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                description='Validation error',
                examples=[
                    OpenApiExample(
                        'Validation Error',
                        value={
                            'email': ['This field is required.'],
                            'password': ['This password is too common.']
                        }
                    )
                ]
            )
        }
    )
    
    def create(self, request, *args, **kwargs):
        """Create a new user and return tokens"""
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.save()
                
                # Generate JWT tokens for the new user
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token
                
                # Update last login
                update_last_login(None, user)
                
                # Return user data with tokens
                user_data = UserSerializer(user).data
                
                logger.info(f"New user registered: {user.email}")
                
                return Response({
                    'message': 'Registration successful',
                    'user': user_data,
                    'tokens': {
                        'access': str(access_token),
                        'refresh': str(refresh),
                    }
                }, status=status.HTTP_201_CREATED)
                
        except ValidationError as e:
            logger.warning(f"Registration validation error: {e}")
            return Response({
                'error': 'Registration failed',
                'details': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return Response({
                'error': 'Registration failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login endpoint using JWT tokens.
    
    Extends the default TokenObtainPairView to include additional user data
    and custom claims in the response.
    """
    serializer_class = CustomTokenObtainPairSerializer
    
    def post(self, request, *args, **kwargs):
        """Login user and return tokens with user data"""
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Get the validated data
            tokens = serializer.validated_data
            user = serializer.user
            
            # Update last login
            update_last_login(None, user)
            
            # Get user profile data
            user_data = UserSerializer(user).data
            
            logger.info(f"User logged in: {user.email}")
            
            return Response({
                'message': 'Login successful',
                'user': user_data,
                'tokens': {
                    'access': tokens['access'],
                    'refresh': tokens['refresh'],
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.warning(f"Login failed: {e}")
            return Response({
                'error': 'Invalid credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)


class UserProfileView(generics.RetrieveAPIView):
    """
    Get current user's profile information.
    
    Returns the authenticated user's profile data including
    personal information and account settings.
    """
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Return the current authenticated user"""
        return self.request.user
    
    def retrieve(self, request, *args, **kwargs):
        """Get user profile"""
        try:
            user = self.get_object()
            serializer = self.get_serializer(user)
            
            return Response({
                'user': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving profile: {e}")
            return Response({
                'error': 'Unable to retrieve profile'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UserProfileUpdateView(generics.UpdateAPIView):
    """
    Update current user's profile information.
    
    Allows authenticated users to update their profile data
    such as name, phone number, and address information.
    """
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Return the current authenticated user"""
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """Update user profile"""
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            updated_user = serializer.save()
            
            # Return updated profile data
            profile_data = UserSerializer(updated_user).data
            
            logger.info(f"Profile updated for user: {user.email}")
            
            return Response({
                'message': 'Profile updated successfully',
                'user': profile_data
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            logger.warning(f"Profile update validation error: {e}")
            return Response({
                'error': 'Profile update failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Profile update error: {e}")
            return Response({
                'error': 'Profile update failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ChangePasswordView(generics.UpdateAPIView):
    """
    Change user's password.
    
    Allows authenticated users to change their password by providing
    their current password and a new password.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        """Return the current authenticated user"""
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        """Change user password"""
        try:
            user = self.get_object()
            serializer = self.get_serializer(user, data=request.data)
            serializer.is_valid(raise_exception=True)
            
            # Password is changed in the serializer's update method
            serializer.save()
            
            logger.info(f"Password changed for user: {user.email}")
            
            return Response({
                'message': 'Password changed successfully'
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            logger.warning(f"Password change validation error: {e}")
            return Response({
                'error': 'Password change failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Password change error: {e}")
            return Response({
                'error': 'Password change failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout endpoint.
    
    Blacklists the provided refresh token to log out the user.
    """
    try:
        refresh_token = request.data.get('refresh_token')
        if not refresh_token:
            return Response({
                'error': 'Refresh token is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        logger.info(f"User logged out: {request.user.email}")
        
        return Response({
            'message': 'Logout successful'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.warning(f"Logout error: {e}")
        return Response({
            'error': 'Invalid token'
        }, status=status.HTTP_400_BAD_REQUEST)


# Admin-only views for user management
class UserListView(generics.ListAPIView):
    """
    List all users (Admin only).
    
    Provides a paginated list of all users in the system.
    Only accessible by staff members.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Only allow staff to access user list"""
        if not self.request.user.is_staff:
            return User.objects.none()
        return super().get_queryset()
    
    def list(self, request, *args, **kwargs):
        """List all users with pagination"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            queryset = self.get_queryset()
            page = self.paginate_queryset(queryset)
            
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'users': serializer.data,
                'total_count': queryset.count()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return Response({
                'error': 'Unable to retrieve user list'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def auth_status_view(request):
    """
    Check authentication status.
    
    Returns information about the current authentication state.
    Useful for frontend applications to check if user is logged in.
    """
    if request.user.is_authenticated:
        user_data = UserSerializer(request.user).data
        return Response({
            'authenticated': True,
            'user': user_data
        }, status=status.HTTP_200_OK)
    else:
        return Response({
            'authenticated': False,
            'user': None
        }, status=status.HTTP_200_OK)
