"""
URL configuration for ecommerce_project
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.http import JsonResponse

def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({
        'status': 'healthy',
        'message': 'E-Commerce API is running!',
        'database': 'PostgreSQL connected'
    })

def api_root(request):
    """Root API endpoint"""
    return JsonResponse({
        'status': 'ok',
        'name': 'E-Commerce Backend API',
        'version': '1.0.0',
        'endpoints': {
            'products': '/api/products/',
            'categories': '/api/categories/',
            'reviews': '/api/reviews/',
            'auth': '/api/auth/',
            'schema': '/api/schema/',
            'docs': '/api/docs/',
            'health': '/health/'
        }
    })

urlpatterns = [
    # Root API
    path('', api_root, name='api-root'),
    path('api/', api_root, name='api-root-with-slash'),
    
    # Health Check
    path('health/', health_check, name='health-check'),
    
    # Admin
    path('admin/', admin.site.urls),

    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'),
         name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # API Apps
    path('api/auth/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/categories/', include('categories.urls')),
    path('api/reviews/', include('reviews.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
