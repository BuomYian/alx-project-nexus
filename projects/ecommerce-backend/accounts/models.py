"""
Models for accounts app
"""

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator


class User(AbstractUser):
    """Extended User model with additional fields"""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    is_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['is_email_verified']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.email

    def get_full_name_or_username(self):
        """Return full name or username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
