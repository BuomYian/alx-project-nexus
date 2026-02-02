from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime
from .models import UserSession, LoginAttempt


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """Custom token serializer with refresh token rotation"""

    def validate(self, attrs):
        data = super().validate(attrs)
        
        # Get the user
        user = User.objects.get(username=attrs.get('username'))
        
        # Log login attempt
        LoginAttempt.objects.create(
            user=user,
            username=user.username,
            ip_address=self.context.get('request').META.get('REMOTE_ADDR', ''),
            user_agent=self.context.get('request').META.get('HTTP_USER_AGENT', ''),
            success=True
        )
        
        # Create user session
        refresh = RefreshToken.for_user(user)
        expires_at = datetime.fromtimestamp(refresh['exp'], tz=timezone.utc)
        UserSession.objects.create(
            user=user,
            refresh_token=str(refresh),
            expires_at=expires_at,
            ip_address=self.context.get('request').META.get('REMOTE_ADDR', ''),
            user_agent=self.context.get('request').META.get('HTTP_USER_AGENT', '')
        )
        
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        
        return data


class UserSerializer(serializers.ModelSerializer):
    """User model serializer"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'is_active')
        read_only_fields = ('id',)


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password_confirm', 'first_name', 'last_name')

    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords do not match")
        
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError("Username already exists")
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("Email already exists")
        
        return data

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class UserSessionSerializer(serializers.ModelSerializer):
    """Serializer for user sessions"""
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserSession
        fields = ('id', 'user', 'is_active', 'created_at', 'expires_at', 'last_used', 'ip_address', 'user_agent')
        read_only_fields = ('id', 'created_at', 'expires_at', 'last_used')


class LoginAttemptSerializer(serializers.ModelSerializer):
    """Serializer for login attempts"""
    class Meta:
        model = LoginAttempt
        fields = ('id', 'username', 'ip_address', 'success', 'attempted_at')
        read_only_fields = ('id', 'attempted_at')


class RefreshTokenSerializer(serializers.Serializer):
    """Serializer for refresh token rotation"""
    refresh = serializers.CharField()
    
    def validate_refresh(self, value):
        try:
            RefreshToken(value)
        except Exception:
            raise serializers.ValidationError("Invalid refresh token")
        return value
