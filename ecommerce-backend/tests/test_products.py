"""
Tests for products app
"""

import pytest
from rest_framework import status
from products.models import Product
from categories.models import Category


@pytest.mark.django_db
class TestProductAPI:
    """Test product API endpoints"""

    def test_list_products(self, api_client, create_product):
        """Test listing products"""
        create_product()
        response = api_client.get('/api/products/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] >= 1

    def test_create_product_authenticated(self, authenticated_client, create_category, create_user):
        """Test creating a product as authenticated user"""
        category = create_category()
        data = {
            'name': 'New Product',
            'description': 'A new test product',
            'sku': 'NEW-001',
            'price': '129.99',
            'quantity_in_stock': 20,
            'category': category.id,
            'image': 'test.jpg'
        }
        response = authenticated_client.post(
            '/api/products/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED

    def test_filter_products_by_category(self, api_client, create_product, create_category):
        """Test filtering products by category"""
        category = create_category(name='Books')
        create_product(category=category)
        response = api_client.get(f'/api/products/?category={category.id}')
        assert response.status_code == status.HTTP_200_OK

    def test_filter_products_by_price(self, api_client, create_product):
        """Test filtering products by price range"""
        create_product(name='Expensive', price='999.99')
        response = api_client.get('/api/products/?min_price=50&max_price=500')
        assert response.status_code == status.HTTP_200_OK

    def test_search_products(self, api_client, create_product):
        """Test searching products"""
        create_product(name='Laptop')
        response = api_client.get('/api/products/?search=laptop')
        assert response.status_code == status.HTTP_200_OK

    def test_sort_products(self, api_client, create_product):
        """Test sorting products"""
        create_product()
        response = api_client.get('/api/products/?ordering=-price')
        assert response.status_code == status.HTTP_200_OK

    def test_product_detail(self, api_client, create_product):
        """Test getting product details"""
        product = create_product()
        response = api_client.get(f'/api/products/{product.id}/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == product.id

    def test_featured_products(self, api_client, create_product):
        """Test getting featured products"""
        create_product()
        response = api_client.get('/api/products/featured/')
        assert response.status_code == status.HTTP_200_OK

    def test_best_sellers(self, api_client, create_product):
        """Test getting best selling products"""
        create_product()
        response = api_client.get('/api/products/best_sellers/')
        assert response.status_code == status.HTTP_200_OK

    def test_top_rated(self, api_client, create_product):
        """Test getting top rated products"""
        create_product()
        response = api_client.get('/api/products/top_rated/')
        assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
class TestCategoryAPI:
    """Test category API endpoints"""

    def test_list_categories(self, api_client, create_category):
        """Test listing categories"""
        create_category()
        response = api_client.get('/api/categories/')
        assert response.status_code == status.HTTP_200_OK

    def test_category_detail(self, api_client, create_category):
        """Test getting category details"""
        category = create_category()
        response = api_client.get(f'/api/categories/{category.id}/')
        assert response.status_code == status.HTTP_200_OK

    def test_search_categories(self, api_client, create_category):
        """Test searching categories"""
        create_category(name='Electronics')
        response = api_client.get('/api/categories/?search=electronics')
        assert response.status_code == status.HTTP_200_OK
