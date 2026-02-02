from django.contrib import admin
from .models import UserSession, LoginAttempt, TokenBlacklistLog


@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_active', 'created_at', 'expires_at', 'ip_address')
    list_filter = ('is_active', 'created_at')
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('created_at', 'last_used', 'refresh_token')

    def has_add_permission(self, request):
        return False


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    list_display = ('username', 'ip_address', 'success', 'attempted_at')
    list_filter = ('success', 'attempted_at')
    search_fields = ('username', 'ip_address')
    readonly_fields = ('username', 'ip_address', 'user_agent', 'attempted_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(TokenBlacklistLog)
class TokenBlacklistLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'token_type', 'blacklisted_at', 'reason')
    list_filter = ('token_type', 'blacklisted_at')
    search_fields = ('user__username', 'jti')
    readonly_fields = ('user', 'jti', 'token_type', 'blacklisted_at')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
