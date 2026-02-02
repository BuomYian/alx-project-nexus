"""
Models for the users app.
"""
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    """Extended user profile model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    cover_image = models.ImageField(upload_to='covers/', null=True, blank=True)
    followers_count = models.IntegerField(default=0)
    following_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Follow(models.Model):
    """Model to track user follows."""
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['follower', 'following']),
            models.Index(fields=['following']),
        ]

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create a profile when a user is created."""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save the profile when the user is saved."""
    if hasattr(instance, 'profile'):
        instance.profile.save()
