"""
Serializers for products app
"""

from rest_framework import serializers
from .models import Product, ProductAttribute
from categories.serializers import CategoryListSerializer


class ProductAttributeSerializer(serializers.ModelSerializer):
    """Serializer for product attributes"""
    class Meta:
        model = ProductAttribute
        fields = ['id', 'attribute_key', 'attribute_value']


class ProductListSerializer(serializers.ModelSerializer):
    """Serializer for product listing (minimal fields)"""
    category = CategoryListSerializer(read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'short_description', 'price',
            'discount_price', 'current_price', 'discount_percentage',
            'image', 'category', 'average_rating', 'review_count',
            'quantity_in_stock', 'is_in_stock', 'is_active', 'is_featured',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at',
                            'average_rating', 'review_count']

    def get_discount_percentage(self, obj):
        return obj.discount_percentage

    def get_current_price(self, obj):
        return str(obj.current_price)


class ProductDetailSerializer(serializers.ModelSerializer):
    """Serializer for product details (all fields)"""
    category = CategoryListSerializer(read_only=True)
    attributes = ProductAttributeSerializer(many=True, read_only=True)
    discount_percentage = serializers.SerializerMethodField()
    current_price = serializers.SerializerMethodField()
    is_in_stock = serializers.BooleanField(read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'short_description',
            'price', 'discount_price', 'current_price', 'discount_percentage',
            'sku', 'category', 'quantity_in_stock', 'is_in_stock', 'image',
            'average_rating', 'review_count', 'sales_count',
            'attributes', 'is_active', 'is_featured', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at',
                            'average_rating', 'review_count', 'slug']

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
            'name', 'description', 'short_description',
            'category', 'sku', 'price', 'discount_price',
            'quantity_in_stock', 'image', 'is_active', 'is_featured',
            'attributes'
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
