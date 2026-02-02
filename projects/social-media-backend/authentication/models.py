from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserSession(models.Model):
    """Track user login sessions with refresh tokens and rotation"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    refresh_token = models.TextField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    last_used = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['refresh_token']),
            models.Index(fields=['expires_at']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

    def is_expired(self):
        """Check if session has expired"""
        return timezone.now() > self.expires_at

    def revoke(self):
        """Revoke this session"""
        self.is_active = False
        self.save()


class LoginAttempt(models.Model):
    """Track failed login attempts for security"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='login_attempts', null=True, blank=True)
    username = models.CharField(max_length=150)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    success = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempted_at']
        indexes = [
            models.Index(fields=['ip_address', 'attempted_at']),
            models.Index(fields=['username', 'success']),
        ]

    def __str__(self):
        return f"{self.username} - {'Success' if self.success else 'Failed'} - {self.attempted_at}"


class TokenBlacklistLog(models.Model):
    """Log blacklisted tokens for audit trail"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='token_blacklists')
    jti = models.CharField(max_length=255, unique=True)
    token_type = models.CharField(max_length=50, choices=[('access', 'Access'), ('refresh', 'Refresh')])
    blacklisted_at = models.DateTimeField(auto_now_add=True)
    reason = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-blacklisted_at']
        indexes = [
            models.Index(fields=['user', 'blacklisted_at']),
            models.Index(fields=['jti']),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.token_type} - {self.blacklisted_at}"
