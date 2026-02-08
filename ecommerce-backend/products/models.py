"""
Models for products app
"""

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator
from django.utils.text import slugify
from categories.models import Category
from accounts.models import User


class Product(models.Model):
    """Product model for e-commerce catalog"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    short_description = models.CharField(max_length=255, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='products'
    )
    sku = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    discount_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )
    quantity_in_stock = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(
        upload_to='products/',
        validators=[FileExtensionValidator(
            allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])]
    )
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    average_rating = models.FloatField(
        default=0.0,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    review_count = models.IntegerField(default=0)
    sales_count = models.IntegerField(default=0)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['price']),
            models.Index(fields=['is_active']),
            models.Index(fields=['-created_at']),
            models.Index(fields=['slug']),
            models.Index(fields=['sku']),
            models.Index(fields=['quantity_in_stock']),
            models.Index(fields=['is_featured']),
            models.Index(fields=['average_rating']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/products/{self.slug}/'

    @property
    def discount_percentage(self):
        """Calculate discount percentage"""
        if self.discount_price and self.discount_price < self.price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def current_price(self):
        """Return current price (discounted if available)"""
        return self.discount_price if self.discount_price else self.price

    @property
    def is_in_stock(self):
        """Check if product is in stock"""
        return self.quantity_in_stock > 0

    def update_review_stats(self):
        """Update review statistics"""
        reviews = self.reviews.all()
        if reviews.exists():
            self.average_rating = reviews.aggregate(
                avg_rating=models.Avg('rating')
            )['avg_rating'] or 0.0
            self.review_count = reviews.count()
            self.save(update_fields=['average_rating', 'review_count'])


class ProductAttribute(models.Model):
    """Product attributes (color, size, brand, etc.)"""
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='attributes'
    )
    attribute_key = models.CharField(max_length=100)  # e.g., 'Color', 'Size'
    attribute_value = models.CharField(max_length=255)  # e.g., 'Red', 'Large'
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_attributes'
        unique_together = ('product', 'attribute_key', 'attribute_value')
        indexes = [
            models.Index(fields=['product']),
            models.Index(fields=['attribute_key']),
        ]

    def __str__(self):
        return f"{self.product.name} - {self.attribute_key}: {self.attribute_value}"
