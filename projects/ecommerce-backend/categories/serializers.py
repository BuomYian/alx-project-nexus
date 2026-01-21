"""
Serializers for categories app
"""

from rest_framework import serializers
from .models import Category


class CategoryListSerializer(serializers.ModelSerializer):
    """Serializer for category listing"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'image', 'is_active']
        read_only_fields = ['id', 'slug']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """Serializer for category details"""
    subcategories = CategoryListSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'image',
            'parent_category', 'subcategories', 'product_count',
            'is_active', 'display_order', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at']

    def get_product_count(self, obj):
        return obj.products.filter(is_active=True).count()


class CategoryCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating categories"""
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent_category',
                  'image', 'is_active', 'display_order']
