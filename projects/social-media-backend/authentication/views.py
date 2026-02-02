from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import cache_page
from .models import UserSession, LoginAttempt, TokenBlacklistLog
from .serializers import (
    CustomTokenObtainPairSerializer,
    UserSerializer,
    UserRegistrationSerializer,
    UserSessionSerializer,
    LoginAttemptSerializer,
    RefreshTokenSerializer
)
from utils.rate_limiting import AuthenticationRateThrottle


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom login endpoint with session tracking and rate limiting"""
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)
    throttle_classes = [AuthenticationRateThrottle]


class CustomTokenRefreshView(TokenRefreshView):
    """Custom token refresh with rotation"""
    permission_classes = (AllowAny,)
    throttle_classes = [AuthenticationRateThrottle]

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                # Mark old session as used and create new one
                try:
                    old_session = UserSession.objects.get(refresh_token=refresh_token, is_active=True)
                    old_session.last_used = timezone.now()
                    old_session.save()
                except UserSession.DoesNotExist:
                    pass
        
        return response


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """User registration endpoint"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Log the registration
        LoginAttempt.objects.create(
            user=user,
            username=user.username,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            success=True
        )
        
        # Generate tokens
        refresh = RefreshToken.for_user(user)
        expires_at = datetime.fromtimestamp(refresh['exp'], tz=timezone.utc)
        
        # Create session
        UserSession.objects.create(
            user=user,
            refresh_token=str(refresh),
            expires_at=expires_at,
            ip_address=request.META.get('REMOTE_ADDR', ''),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout endpoint - revoke refresh tokens"""
    try:
        refresh_token = request.data.get('refresh')
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()
            
            # Mark session as inactive
            UserSession.objects.filter(refresh_token=refresh_token).update(is_active=False)
            
            # Log token blacklist
            TokenBlacklistLog.objects.create(
                user=request.user,
                jti=token.get('jti', ''),
                token_type='refresh',
                reason='User logout'
            )
            
            return Response({'detail': 'Successfully logged out'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Refresh token required'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_all(request):
    """Logout from all devices - revoke all refresh tokens"""
    try:
        sessions = UserSession.objects.filter(user=request.user, is_active=True)
        count = sessions.count()
        
        for session in sessions:
            session.revoke()
            TokenBlacklistLog.objects.create(
                user=request.user,
                jti='all',
                token_type='refresh',
                reason='Logout from all devices'
            )
        
        return Response(
            {'detail': f'Logged out from {count} device(s)'},
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """User management viewset"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=self.request.user.id)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['put', 'patch'], permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        """Update current user profile"""
        serializer = self.get_serializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Change user password"""
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not user.check_password(old_password):
            return Response({'detail': 'Invalid old password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()
        
        # Logout from all devices after password change
        UserSession.objects.filter(user=user, is_active=True).update(is_active=False)
        
        return Response({'detail': 'Password changed successfully. Please login again.'})


class UserSessionViewSet(viewsets.ModelViewSet):
    """Manage user sessions"""
    serializer_class = UserSessionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return UserSession.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def revoke(self, request, pk=None):
        """Revoke a specific session"""
        session = self.get_object()
        if session.user != request.user:
            return Response(
                {'detail': 'Not authorized to revoke this session'},
                status=status.HTTP_403_FORBIDDEN
            )
        session.revoke()
        return Response({'detail': 'Session revoked'})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def active_sessions(self, request):
        """Get all active sessions for current user"""
        sessions = UserSession.objects.filter(user=request.user, is_active=True)
        serializer = self.get_serializer(sessions, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['delete'], permission_classes=[IsAuthenticated])
    def clear_expired(self, request):
        """Delete all expired sessions"""
        expired = UserSession.objects.filter(
            user=request.user,
            expires_at__lt=timezone.now()
        ).delete()
        return Response({'deleted': expired[0]})
