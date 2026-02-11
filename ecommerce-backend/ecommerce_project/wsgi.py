"""
WSGI config for ecommerce_project
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')

try:
    application = get_wsgi_application()
    print("✅ WSGI application initialized successfully", file=sys.stderr)
except Exception as e:
    print(f"❌ WSGI initialization error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    raise
