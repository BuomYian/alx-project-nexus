"""
Filters for products app
"""

import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    """Filter set for products"""
    min_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='gte'
    )
    max_price = django_filters.NumberFilter(
        field_name='price',
        lookup_expr='lte'
    )
    min_rating = django_filters.NumberFilter(
        field_name='average_rating',
        lookup_expr='gte'
    )
    category_name = django_filters.CharFilter(
        field_name='category__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Product
        fields = ['category', 'is_active', 'is_featured']
