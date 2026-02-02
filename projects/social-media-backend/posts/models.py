"""
Models for the posts app.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db.models import Count, Q


class Post(models.Model):
    """Post model for social media content."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['is_published', '-created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.author.username}: {self.title[:50]}"

    @property
    def like_count(self):
        """Get total likes for this post."""
        return self.likes.count()

    @property
    def comment_count(self):
        """Get total comments for this post."""
        return self.comments.count()

    def get_like_count(self):
        """Get like count efficiently."""
        return self.likes.count()

    def get_comment_count(self):
        """Get comment count efficiently."""
        return self.comments.count()


class Comment(models.Model):
    """Comment model for post discussions."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        related_name='replies',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_edited = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['post', '-created_at']),
            models.Index(fields=['author']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.author.username} on {self.post.title[:30]}"

    @property
    def like_count(self):
        """Get total likes for this comment."""
        return self.comment_likes.count()

    def get_like_count(self):
        """Get like count efficiently."""
        return self.comment_likes.count()
