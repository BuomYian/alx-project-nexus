"""
Custom middleware for error logging and debugging
"""

import sys
import traceback
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)


class ErrorLoggingMiddleware:
    """Log all errors to stderr for Railway debugging"""
    
    def __init__(self, get_response):
        self.get_response = get_response
        print("✅ ErrorLoggingMiddleware initialized", file=sys.stderr)
    
    def __call__(self, request):
        try:
            print(f"📥 Request: {request.method} {request.path}", file=sys.stderr)
            response = self.get_response(request)
            print(f"✅ Response: {response.status_code}", file=sys.stderr)
            return response
        except Exception as e:
            error_msg = f"❌ ERROR: {request.method} {request.path} - {type(e).__name__}: {str(e)}"
            print(error_msg, file=sys.stderr)
            logger.exception(error_msg)
            traceback.print_exc(file=sys.stderr)
            
            # Return JSON error response
            try:
                return JsonResponse({
                    'status': 'error',
                    'message': str(e),
                    'type': type(e).__name__,
                    'path': request.path
                }, status=500)
            except Exception as json_error:
                print(f"❌ Failed to create error response: {json_error}", file=sys.stderr)
                return JsonResponse({'status': 'error', 'message': 'Internal Server Error'}, status=500)

