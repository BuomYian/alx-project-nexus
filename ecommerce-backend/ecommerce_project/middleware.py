"""
Custom middleware for error logging and debugging
"""

import sys
import traceback
from django.http import JsonResponse


class ErrorLoggingMiddleware:
    """Log all errors to stderr for Railway debugging"""
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            print(f"❌ ERROR in {request.method} {request.path}", file=sys.stderr)
            print(f"   Exception: {type(e).__name__}: {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            
            # Return JSON error response
            return JsonResponse({
                'status': 'error',
                'message': str(e),
                'type': type(e).__name__
            }, status=500)
