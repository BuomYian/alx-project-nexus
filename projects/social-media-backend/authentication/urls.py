from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView
from .views import (
    CustomTokenObtainPairView,
    CustomTokenRefreshView,
    register,
    logout,
    logout_all,
    UserViewSet,
    UserSessionViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'sessions', UserSessionViewSet, basename='session')

urlpatterns = [
    # Auth endpoints
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('register/', register, name='register'),
    path('logout/', logout, name='logout'),
    path('logout-all/', logout_all, name='logout_all'),
    
    # User and session management
    path('', include(router.urls)),
]
