"""
Admin configuration for products app
"""

from django.contrib import admin
from .models import Product, ProductAttribute


class ProductAttributeInline(admin.TabularInline):
    """Inline admin for product attributes"""
    model = ProductAttribute
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Product admin"""
    list_display = ('name', 'sku', 'category', 'price',
                    'quantity_in_stock', 'is_active', 'created_at')
    list_filter = ('is_active', 'is_featured', 'category', 'created_at')
    search_fields = ('name', 'description', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('average_rating', 'review_count',
                       'sales_count', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'short_description', 'sku')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'quantity_in_stock')
        }),
        ('Classification', {
            'fields': ('category', 'is_active', 'is_featured')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Statistics', {
            'fields': ('average_rating', 'review_count', 'sales_count')
        }),
        ('Metadata', {
            'fields': ('created_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [ProductAttributeInline]
    ordering = ('-created_at',)
