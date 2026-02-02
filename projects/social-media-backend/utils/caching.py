"""
Caching utilities and decorators for the social media platform.
"""
from functools import wraps
from django.core.cache import cache
from django.views.decorators.cache import cache_page as django_cache_page
from django.views.decorators.vary import vary_on_headers
import hashlib
import json


def cache_key(*args, **kwargs):
    """Generate a cache key from function arguments."""
    key_parts = [str(arg) for arg in args] + [f"{k}={v}" for k, v in sorted(kwargs.items())]
    key_string = "|".join(key_parts)
    return hashlib.md5(key_string.encode()).hexdigest()


def cache_result(timeout=300, key_func=None):
    """
    Decorator to cache function results.
    
    Args:
        timeout: Cache timeout in seconds (default 5 minutes)
        key_func: Optional custom function to generate cache key
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if key_func:
                cache_key_str = key_func(*args, **kwargs)
            else:
                cache_key_str = f"{func.__module__}.{func.__name__}:{cache_key(*args, **kwargs)}"
            
            # Try to get from cache
            result = cache.get(cache_key_str)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache.set(cache_key_str, result, timeout)
            return result
        return wrapper
    return decorator


def invalidate_cache(*patterns):
    """
    Invalidate cache entries matching patterns.
    
    Args:
        *patterns: Cache key patterns to invalidate
    """
    for pattern in patterns:
        # For Redis, we would use pattern deletion
        # For now, use simple key deletion
        try:
            cache.delete(pattern)
        except Exception:
            pass


class CacheableMixin:
    """Mixin for querysets to add caching capabilities."""
    
    _cache_key = None
    _cache_timeout = 300
    
    def set_cache_key(self, key):
        """Set custom cache key."""
        self._cache_key = key
        return self
    
    def set_cache_timeout(self, timeout):
        """Set cache timeout in seconds."""
        self._cache_timeout = timeout
        return self
    
    def get_cached(self):
        """Get cached results if available."""
        if not self._cache_key:
            return None
        return cache.get(self._cache_key)
    
    def cache_result(self, data):
        """Cache query results."""
        if self._cache_key:
            cache.set(self._cache_key, data, self._cache_timeout)
        return data


def cache_page_for_anonymous(timeout=300):
    """Cache page for anonymous users only."""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated:
                # Don't cache for authenticated users
                return view_func(request, *args, **kwargs)
            return django_cache_page(timeout)(view_func)(request, *args, **kwargs)
        return wrapper
    return decorator


def get_cached_or_fetch(cache_key, fetch_func, timeout=300):
    """Get value from cache or fetch if not cached."""
    value = cache.get(cache_key)
    if value is None:
        value = fetch_func()
        cache.set(cache_key, value, timeout)
    return value


def invalidate_user_cache(user_id):
    """Invalidate all cache entries for a user."""
    patterns = [
        f"user_{user_id}:*",
        f"feed_{user_id}:*",
        f"profile_{user_id}:*",
    ]
    invalidate_cache(*patterns)


def invalidate_post_cache(post_id):
    """Invalidate all cache entries related to a post."""
    patterns = [
        f"post_{post_id}:*",
        f"comments_post_{post_id}:*",
        f"likes_post_{post_id}:*",
    ]
    invalidate_cache(*patterns)
