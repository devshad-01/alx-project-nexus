"""
Authentication serializers for ALX Project Nexus E-Commerce Backend
Handles user registration, authentication, and profile management
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from drf_spectacular.utils import extend_schema_field
from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration with validation
    """
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Password must be at least 8 characters long"
    )
    password_confirm = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'},
        help_text="Confirm your password"
    )
    username = serializers.CharField(
        required=False,
        help_text="Username (will be auto-generated from email if not provided)"
    )

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'password', 'password_confirm'
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password_confirm': {'write_only': True},
        }

    def validate_email(self, value):
        """
        Validate email uniqueness
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        """
        Validate username uniqueness and format (if provided)
        """
        if value:  # Only validate if username is provided
            if User.objects.filter(username=value).exists():
                raise serializers.ValidationError("A user with this username already exists.")
            
            if len(value) < 3:
                raise serializers.ValidationError("Username must be at least 3 characters long.")
        
        return value

    def validate_password(self, value):
        """
        Validate password strength
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """
        Validate password confirmation
        """
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({
                'password_confirm': "Password fields didn't match."
            })
        return attrs

    def create(self, validated_data):
        """
        Create new user with encrypted password
        """
        # Remove password_confirm from validated_data
        validated_data.pop('password_confirm', None)
        
        # Auto-generate username from email if not provided
        if not validated_data.get('username'):
            email = validated_data['email']
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            
            # Ensure username is unique by adding counter if needed
            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1
            
            validated_data['username'] = username
        
        # Create user with encrypted password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for user profile information
    """
    full_name = serializers.SerializerMethodField()
    age = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'full_name', 'age',
            'is_active', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'username', 'date_joined', 'last_login']

    @extend_schema_field(serializers.CharField)
    def get_full_name(self, obj):
        """
        Get user's full name
        """
        return f"{obj.first_name} {obj.last_name}".strip()

    @extend_schema_field(serializers.IntegerField)
    def get_age(self, obj):
        """
        Calculate user's age from date of birth
        """
        # Since our User model doesn't have date_of_birth, return None
        return None


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating user profile
    """
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = [
            'email', 'first_name', 'last_name'
        ]

    def validate_email(self, value):
        """
        Validate email uniqueness (excluding current user)
        """
        user = self.instance
        if User.objects.filter(email=value).exclude(pk=user.pk).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value


class ChangePasswordSerializer(serializers.Serializer):
    """
    Serializer for changing user password
    """
    old_password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Current password"
    )
    new_password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="New password"
    )
    new_password_confirm = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Confirm new password"
    )

    def validate_old_password(self, value):
        """
        Validate current password
        """
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate_new_password(self, value):
        """
        Validate new password strength
        """
        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value

    def validate(self, attrs):
        """
        Validate new password confirmation
        """
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': "New password fields didn't match."
            })
        return attrs

    def save(self, **kwargs):
        """
        Update user password
        """
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT token serializer with additional user information
    """
    
    @classmethod
    def get_token(cls, user):
        """
        Add custom claims to JWT token
        """
        token = super().get_token(user)
        
        # Add custom claims
        token['user_id'] = user.id
        token['username'] = user.username
        token['email'] = user.email
        token['full_name'] = f"{user.first_name} {user.last_name}".strip()
        token['is_staff'] = user.is_staff
        
        return token

    def validate(self, attrs):
        """
        Validate credentials and return tokens with user data
        """
        data = super().validate(attrs)
        
        # Add user data to response
        data['user'] = {
            'id': self.user.id,
            'username': self.user.username,
            'email': self.user.email,
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'full_name': f"{self.user.first_name} {self.user.last_name}".strip(),
            'is_staff': self.user.is_staff,
            'is_active': self.user.is_active,
        }
        
        return data


class UserLoginSerializer(serializers.Serializer):
    """
    Serializer for user login with username/email
    """
    username_or_email = serializers.CharField(
        help_text="Username or email address"
    )
    password = serializers.CharField(
        style={'input_type': 'password'},
        help_text="Password"
    )

    def validate(self, attrs):
        """
        Validate login credentials
        """
        username_or_email = attrs.get('username_or_email')
        password = attrs.get('password')

        if username_or_email and password:
            # Try to find user by username or email
            user = None
            if '@' in username_or_email:
                # It's an email
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request=self.context.get('request'),
                                     username=user_obj.username, password=password)
                except User.DoesNotExist:
                    pass
            else:
                # It's a username
                user = authenticate(request=self.context.get('request'),
                                 username=username_or_email, password=password)

            if not user:
                msg = 'Unable to log in with provided credentials.'
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = 'User account is disabled.'
                raise serializers.ValidationError(msg, code='authorization')

            attrs['user'] = user
            return attrs
        else:
            msg = 'Must include "username_or_email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')


class PasswordResetSerializer(serializers.Serializer):
    """
    Serializer for password reset request
    """
    email = serializers.EmailField(
        help_text="Email address associated with your account"
    )

    def validate_email(self, value):
        """
        Validate email exists in system
        """
        try:
            User.objects.get(email=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("No user found with this email address.")
        return value
