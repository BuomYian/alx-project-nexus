from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from .models import UserSession
import logging

logger = logging.getLogger(__name__)


class SessionManagementMiddleware(MiddlewareMixin):
    """Middleware to manage JWT sessions and track user activity"""

    def process_request(self, request):
        """Update session last_used timestamp"""
        if hasattr(request, 'user') and request.user.is_authenticated:
            # Extract token from Authorization header
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                token = auth_header[7:]
                try:
                    # Try to update session last_used
                    # Note: In a real scenario, you'd decode the JWT to get the session ID
                    # For now, we just update all active sessions
                    UserSession.objects.filter(
                        user=request.user,
                        is_active=True,
                        expires_at__gt=timezone.now()
                    ).update(last_used=timezone.now())
                except Exception as e:
                    logger.warning(f"Error updating session: {str(e)}")

        return None

    def process_response(self, request, response):
        """Clean up expired sessions periodically"""
        # Clean expired sessions once per hour (you could use Celery for this too)
        if hasattr(request, 'user') and request.user.is_authenticated:
            try:
                UserSession.objects.filter(
                    user=request.user,
                    expires_at__lt=timezone.now()
                ).delete()
            except Exception as e:
                logger.warning(f"Error cleaning expired sessions: {str(e)}")

        return response
