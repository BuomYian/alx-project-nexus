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
    return JsonResponse({"status": "ok"})

def api_root(request):
    return JsonResponse({
        'status': 'ok',
        'name': 'E-Commerce Backend API',
        'version': '1.0.0',
        'endpoints': {
            'products': '/api/products/',
            'categories': '/api/categories/',
            'reviews': '/api/reviews/',
            'auth': '/api/auth/',
            'docs': '/api/docs/',
            'redoc': '/api/redoc/',
            'health': '/'
        }
    })

urlpatterns = [
    # Root & Health
    path('', health_check, name='health-check'),
    path('api/', api_root, name='api-root'),
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
