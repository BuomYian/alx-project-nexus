"""
Rate limiting utilities and decorators for API endpoints.
"""
from functools import wraps
from django.core.cache import cache
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from rest_framework.throttling import SimpleRateThrottle, UserRateThrottle
from rest_framework.response import Response
from rest_framework import status
import time


class CustomUserRateThrottle(UserRateThrottle):
    """
    Custom rate throttle for authenticated users.
    Rate: 1000 requests per day, 100 per hour
    """
    scope = 'user'
    THROTTLE_RATES = {
        'user': '1000/day',
    }


class CustomAnonRateThrottle(SimpleRateThrottle):
    """
    Custom rate throttle for anonymous users.
    Rate: 100 requests per day
    """
    scope = 'anon'
    THROTTLE_RATES = {
        'anon': '100/day',
    }
    
    def get_ident(self, request):
        """Get client IP address for rate limiting."""
        return request.META.get('REMOTE_ADDR', '')


class SearchRateThrottle(UserRateThrottle):
    """Rate throttle for search endpoints."""
    scope = 'search'
    THROTTLE_RATES = {
        'search': '100/hour',
    }


class AuthenticationRateThrottle(SimpleRateThrottle):
    """Rate throttle for authentication endpoints (stricter)."""
    scope = 'auth'
    THROTTLE_RATES = {
        'auth': '5/minute',  # 5 attempts per minute
    }
    
    def get_ident(self, request):
        """Get client IP address."""
        return request.META.get('REMOTE_ADDR', '')


class UploadRateThrottle(UserRateThrottle):
    """Rate throttle for upload endpoints."""
    scope = 'upload'
    THROTTLE_RATES = {
        'upload': '10/hour',  # 10 uploads per hour
    }


def rate_limit(key_func=None, limit=10, period=60):
    """
    Decorator for rate limiting function calls.
    
    Args:
        key_func: Function to generate rate limit key (receives request)
        limit: Number of allowed requests
        period: Time period in seconds
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            # Generate rate limit key
            if key_func:
                rate_key = key_func(request)
            else:
                if request.user.is_authenticated:
                    rate_key = f"rate_limit:{view_func.__name__}:user:{request.user.id}"
                else:
                    rate_key = f"rate_limit:{view_func.__name__}:ip:{request.META.get('REMOTE_ADDR')}"
            
            # Get current count
            current_count = cache.get(rate_key, 0)
            
            if current_count >= limit:
                return JsonResponse(
                    {'error': 'Rate limit exceeded. Please try again later.'},
                    status=429
                )
            
            # Increment and set expiry
            cache.set(rate_key, current_count + 1, period)
            
            response = view_func(request, *args, **kwargs)
            
            # Add rate limit headers
            response['X-RateLimit-Limit'] = str(limit)
            response['X-RateLimit-Remaining'] = str(limit - current_count - 1)
            response['X-RateLimit-Reset'] = str(int(time.time()) + period)
            
            return response
        return wrapper
    return decorator


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class RateLimitMiddleware:
    """Middleware for global rate limiting."""
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.whitelist = ['/admin/', '/static/', '/media/']
    
    def __call__(self, request):
        # Check if URL is in whitelist
        if any(request.path.startswith(path) for path in self.whitelist):
            return self.get_response(request)
        
        # Get client identifier
        if request.user.is_authenticated:
            client_id = f"user:{request.user.id}"
        else:
            client_id = f"ip:{get_client_ip(request)}"
        
        # Rate limit key
        rate_key = f"global_rate_limit:{client_id}:{request.method}:{request.path}"
        
        # Get current count
        current_count = cache.get(rate_key, 0)
        
        # Global limit: 100 requests per minute per client
        if current_count >= 100:
            return JsonResponse(
                {'error': 'Rate limit exceeded'},
                status=429
            )
        
        cache.set(rate_key, current_count + 1, 60)
        return self.get_response(request)


class APIRateLimitMixin:
    """Mixin for ViewSets to add rate limiting."""
    
    throttle_classes = []
    
    def get_throttle_classes(self, action):
        """Get throttle classes for specific action."""
        if action == 'create':
            return [UploadRateThrottle]
        elif action == 'list':
            return [SearchRateThrottle]
        return self.throttle_classes
