"""
URL configuration for accounts app
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CustomTokenObtainPairView, UserViewSet
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/',
         UserViewSet.as_view({'post': 'create'}), name='register'),
]
