"""
URL configuration for reviews app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ReviewViewSet

router = DefaultRouter()
router.register(r'', ReviewViewSet, basename='review')

urlpatterns = [
    path('', include(router.urls)),
    path('products/<int:product_id>/reviews/', ReviewViewSet.as_view({
        'get': 'list',
        'post': 'create'
    }), name='product_reviews'),
]
