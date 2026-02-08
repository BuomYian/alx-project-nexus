"""
Models for reviews app
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from products.models import Product
from accounts.models import User


class Review(models.Model):
    """Product review and rating model"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    title = models.CharField(max_length=200)
    comment = models.TextField()
    is_verified_purchase = models.BooleanField(default=False)
    helpful_count = models.IntegerField(default=0)
    unhelpful_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reviews'
        unique_together = ('product', 'user')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['user']),
            models.Index(fields=['rating']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_verified_purchase']),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        # Update product review stats when review is created or updated
        if is_new:
            self.product.update_review_stats()

    def delete(self, *args, **kwargs):
        product = self.product
        super().delete(*args, **kwargs)

        # Update product review stats when review is deleted
        product.update_review_stats()

    def __str__(self):
        return f"Review of {self.product.name} by {self.user.email} - {self.rating}★"
