"""
Models for the posts app.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import URLValidator
from django.db.models import Count, Q
from django.contrib.postgres.search import SearchVectorField, SearchVector
from django.contrib.postgres.indexes import GinIndex


class Hashtag(models.Model):
    """Model for hashtags used in posts."""
    tag = models.CharField(max_length=100, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Hashtags"
    
    def __str__(self):
        return f"#{self.tag}"
    
    @property
    def post_count(self):
        """Get count of posts using this hashtag."""
        return self.posts.count()


class Mention(models.Model):
    """Model for user mentions in posts."""
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='mentions')
    mentioned_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentions_received')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('post', 'mentioned_user')
        indexes = [
            models.Index(fields=['mentioned_user', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.post.author.username} mentioned {self.mentioned_user.username}"


class Post(models.Model):
    """Post model for social media content with full-text search support."""
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    hashtags = models.ManyToManyField(Hashtag, related_name='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=True, db_index=True)
    search_vector = SearchVectorField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['author', '-created_at']),
            models.Index(fields=['is_published', '-created_at']),
            models.Index(fields=['created_at']),
            GinIndex(fields=['search_vector']),  # PostgreSQL GIN index for FTS
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
    
    def extract_hashtags(self):
        """Extract hashtags from content and title."""
        import re
        text = f"{self.title} {self.content}"
        hashtag_pattern = r'#(\w+)'
        tags = re.findall(hashtag_pattern, text)
        
        for tag in tags:
            hashtag, _ = Hashtag.objects.get_or_create(tag=tag.lower())
            self.hashtags.add(hashtag)
    
    def extract_mentions(self):
        """Extract user mentions from content and title."""
        import re
        text = f"{self.title} {self.content}"
        mention_pattern = r'@(\w+)'
        mentions = re.findall(mention_pattern, text)
        
        for mention in mentions:
            try:
                user = User.objects.get(username=mention)
                Mention.objects.get_or_create(post=self, mentioned_user=user)
            except User.DoesNotExist:
                pass
    
    def save(self, *args, **kwargs):
        """Override save to update search vector."""
        super().save(*args, **kwargs)
        # Update search vector for full-text search
        self.__class__.objects.filter(pk=self.pk).update(
            search_vector=SearchVector('title', weight='A') + SearchVector('content', weight='B')
        )



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
