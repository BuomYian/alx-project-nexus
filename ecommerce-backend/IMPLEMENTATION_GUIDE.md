# E-Commerce Backend - Implementation Guide

## Table of Contents
1. [Project Setup](#project-setup)
2. [Step-by-Step Implementation](#step-by-step-implementation)
3. [Code Examples](#code-examples)
4. [Common Challenges & Solutions](#common-challenges--solutions)
5. [Performance Tips](#performance-tips)
6. [Deployment Guide](#deployment-guide)

---

## Project Setup

### Initial Setup Steps

#### 1. Create Project Directory
```bash
mkdir ecommerce-backend
cd ecommerce-backend
```

#### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 3. Install Dependencies
Create `requirements.txt`:
```
Django==4.2.0
djangorestframework==3.14.0
django-cors-headers==4.0.0
django-filter==23.1
djangorestframework-simplejwt==5.2.2
psycopg2-binary==2.9.6
drf-spectacular==0.26.2
python-dotenv==1.0.0
pytest==7.3.1
pytest-django==4.5.2
pytest-cov==4.1.0
```

Install dependencies:
```bash
pip install -r requirements.txt
```

#### 4. Create Django Project
```bash
django-admin startproject ecommerce_project .
django-admin startapp accounts
django-admin startapp products
django-admin startapp categories
django-admin startapp reviews
```

#### 5. Configure Environment Variables
Create `.env` file:
```
# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Settings
JWT_SECRET_KEY=your-jwt-secret-key
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Email Configuration (optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## Step-by-Step Implementation

### Phase 1: Database Models & Schema

#### 1.1 User Model (`accounts/models.py`)

```python
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Extended User model with additional fields"""
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['is_verified']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        return self.email
```

#### 1.2 Category Model (`categories/models.py`)

```python
from django.db import models
from django.utils.text import slugify

class Category(models.Model):
    """Product category model"""
    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    parent_category = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subcategories'
    )
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'
        ordering = ['display_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
            models.Index(fields=['parent_category']),
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
```

#### 1.3 Product Model (`products/models.py`)

```python
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from categories.models import Category
from accounts.models import User

class Product(models.Model):
    """Product model for e-commerce catalog"""
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
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
        blank=True
    )
    quantity_in_stock = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='products/')
    is_active = models.BooleanField(default=True)
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
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def discount_percentage(self):
        if self.discount_price:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0

    @property
    def current_price(self):
        return self.discount_price if self.discount_price else self.price


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
```

#### 1.4 Review Model (`reviews/models.py`)

```python
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
        ]

    def __str__(self):
        return f"Review of {self.product.name} by {self.user.email}"
```

---

### Phase 2: Serializers & Validation

#### 2.1 Product Serializer (`products/serializers.py`)

```python
from rest_framework import serializers
from .models import Product, ProductAttribute
from categories.models import Category

class ProductAttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ['id', 'attribute_key', 'attribute_value']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product listing (minimal fields)"""
    category = CategorySerializer(read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price',
            'discount_price', 'current_price', 'discount_percentage',
            'image', 'category', 'average_rating', 'review_count',
            'quantity_in_stock', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_discount_percentage(self, obj):
        return obj.discount_percentage

    def get_current_price(self, obj):
        return str(obj.current_price)


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product details (all fields)"""
    category = CategorySerializer(read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    reviews = serializers.SerializerMethodField()
    discount_percentage = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'discount_price', 'current_price', 'discount_percentage',
            'sku', 'category', 'quantity_in_stock', 'image',
            'average_rating', 'review_count', 'sales_count',
            'attributes', 'reviews', 'is_active', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'average_rating', 'review_count']

    def get_reviews(self, obj):
        reviews = obj.reviews.all()[:5]  # Get latest 5 reviews
        from reviews.serializers import ReviewSerializer
        return ReviewSerializer(reviews, many=True).data

    def get_discount_percentage(self, obj):
        return obj.discount_percentage

    def get_current_price(self, obj):
        return str(obj.current_price)


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating products"""
    attributes = ProductAttributeSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            'name', 'slug', 'description', 'short_description',
            'category', 'sku', 'price', 'discount_price',
            'quantity_in_stock', 'image', 'is_active', 'attributes'
        ]

    def create(self, validated_data):
        attributes_data = validated_data.pop('attributes', [])
        product = Product.objects.create(**validated_data)
        
        for attr_data in attributes_data:
            ProductAttribute.objects.create(product=product, **attr_data)
        
        return product

    def update(self, instance, validated_data):
        attributes_data = validated_data.pop('attributes', None)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        if attributes_data is not None:
            instance.attributes.all().delete()
            for attr_data in attributes_data:
                ProductAttribute.objects.create(product=instance, **attr_data)
        
        return instance
```

---

### Phase 3: Views & ViewSets

#### 3.1 Product ViewSet (`products/views.py`)

```python
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    ProductCreateUpdateSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for product CRUD operations with filtering and pagination"""
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'price', 'is_active']
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'sales_count', 'average_rating']
    ordering = ['-created_at']
    pagination_class = 'pagination.CustomPagination'

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Filter by price range
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        return queryset.select_related('category').prefetch_related('attributes')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def add_to_wishlist(self, request, pk=None):
        """Add product to user's wishlist"""
        product = self.get_object()
        user = request.user
        
        if user.wishlist.filter(pk=product.pk).exists():
            return Response(
                {'detail': 'Product already in wishlist'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.wishlist.add(product)
        return Response({'detail': 'Product added to wishlist'})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def featured(self, request):
        """Get featured products"""
        products = self.get_queryset().order_by('-sales_count')[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
```

---

### Phase 4: Authentication Setup

#### 4.1 JWT Configuration (`ecommerce_project/settings.py`)

```python
from datetime import timedelta
from pathlib import Path
import os
from dotenv import load_dotenv

load_dotenv()

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_filters',
    'drf_spectacular',
    
    'accounts',
    'products',
    'categories',
    'reviews',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=int(os.getenv('JWT_EXPIRATION_HOURS', 24))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('JWT_SECRET_KEY'),
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'E-Commerce Backend API',
    'DESCRIPTION': 'RESTful API for e-commerce platform',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'AUTHENTICATION_SCHEMES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ],
}
```

#### 4.2 Authentication Serializers (`accounts/serializers.py`)

```python
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'password2', 'first_name', 'last_name']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({'password': 'Passwords must match'})
        return data

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'created_at']
        read_only_fields = ['id', 'created_at']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token
```

---

## Code Examples

### Example 1: Filtering Products by Price Range

```bash
# Get products between $100 and $500
curl -X GET "http://localhost:8000/api/products/?min_price=100&max_price=500"
```

### Example 2: Sorting Products

```bash
# Sort by price (ascending)
curl -X GET "http://localhost:8000/api/products/?ordering=price"

# Sort by price (descending)
curl -X GET "http://localhost:8000/api/products/?ordering=-price"

# Sort by creation date
curl -X GET "http://localhost:8000/api/products/?ordering=-created_at"
```

### Example 3: Pagination

```bash
# Page 2 with 20 items per page
curl -X GET "http://localhost:8000/api/products/?page=2&page_size=20"
```

### Example 4: Searching Products

```bash
# Search for "laptop" in product name and description
curl -X GET "http://localhost:8000/api/products/?search=laptop"
```

### Example 5: Authentication Flow

```bash
# Register new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password2": "SecurePass123"
  }'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'

# Use token in subsequent requests
curl -X GET http://localhost:8000/api/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## Common Challenges & Solutions

### Challenge 1: Slow Product List Queries

**Problem**: When listing products with categories and attributes, queries are slow.

**Solution**: Use `select_related()` and `prefetch_related()`:

```python
# Good - Optimized query
queryset = Product.objects.select_related('category').prefetch_related('attributes')

# Bad - Multiple database hits
queryset = Product.objects.all()
```

### Challenge 2: Duplicate Reviews

**Problem**: Users can submit multiple reviews for the same product.

**Solution**: Use unique constraint in model:

```python
class Meta:
    unique_together = ('product', 'user')
```

### Challenge 3: Price Range Filtering Not Working

**Problem**: Filtering by `min_price` and `max_price` doesn't work properly.

**Solution**: Handle in `get_queryset()` method:

```python
def get_queryset(self):
    queryset = super().get_queryset()
    min_price = self.request.query_params.get('min_price')
    max_price = self.request.query_params.get('max_price')
    
    if min_price:
        queryset = queryset.filter(price__gte=float(min_price))
    if max_price:
        queryset = queryset.filter(price__lte=float(max_price))
    
    return queryset
```

### Challenge 4: Authentication Not Working in Swagger

**Problem**: JWT token not being sent in Swagger docs.

**Solution**: Configure Swagger with proper authentication:

```python
SPECTACULAR_SETTINGS = {
    'SECURITY_SCHEMES': {
        'bearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    },
    'SECURITY': [{'bearerAuth': []}],
}
```

---

## Performance Tips

### 1. Database Indexing
```python
class Meta:
    indexes = [
        models.Index(fields=['category']),
        models.Index(fields=['price']),
        models.Index(fields=['is_active']),
        models.Index(fields=['-created_at']),
    ]
```

### 2. Query Optimization
```python
# Use select_related for ForeignKey and OneToOneField
queryset = Product.objects.select_related('category')

# Use prefetch_related for reverse ForeignKey and ManyToManyField
queryset = Product.objects.prefetch_related('reviews')

# Use only() to fetch specific fields
queryset = Product.objects.only('id', 'name', 'price')
```

### 3. Pagination
```python
# Always paginate to limit data transfer
class CustomPagination(PageNumberPagination):
    page_size = 20
    max_page_size = 100
```

### 4. Caching
```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
@api_view(['GET'])
def get_products(request):
    pass
```

---

## Deployment Guide

### 1. Prepare for Production

Update `settings.py`:
```python
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

### 2. Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### 3. Run Migrations
```bash
python manage.py migrate
```

### 4. Deploy to Heroku
```bash
heroku create your-app-name
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
git push heroku main
heroku run python manage.py migrate
```

### 5. Verify Deployment
```bash
curl https://your-app-name.herokuapp.com/api/products/
```

---

**For more details, see the main README.md**
