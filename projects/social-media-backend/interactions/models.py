"""
Models for the interactions app.
"""
from django.db import models
from django.contrib.auth.models import User
from posts.models import Post, Comment


class PostLike(models.Model):
    """Model to track post likes."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_posts')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('post', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.post.title[:30]}"


class CommentLike(models.Model):
    """Model to track comment likes."""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('comment', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['comment']),
            models.Index(fields=['user']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.comment.content[:30]}"


class Share(models.Model):
    """Model to track post shares."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='shares')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_posts')
    shared_at = models.DateTimeField(auto_now_add=True)
    share_message = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-shared_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['shared_at']),
        ]

    def __str__(self):
        return f"{self.user.username} shared {self.post.title[:30]}"


class View(models.Model):
    """Model to track post views for analytics."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='views')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='viewed_posts', null=True, blank=True)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-viewed_at']
        indexes = [
            models.Index(fields=['post']),
            models.Index(fields=['user']),
            models.Index(fields=['viewed_at']),
        ]

    def __str__(self):
        user_display = self.user.username if self.user else "Anonymous"
        return f"{user_display} viewed {self.post.title[:30]}"


class Notification(models.Model):
    """Model for user notifications."""
    NOTIFICATION_TYPES = (
        ('like', 'Like'),
        ('comment', 'Comment'),
        ('follow', 'Follow'),
        ('share', 'Share'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='actions')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['user', 'is_read']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.actor.username} {self.notification_type}d {self.user.username}"
