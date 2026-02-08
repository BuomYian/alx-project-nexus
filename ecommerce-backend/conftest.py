"""
Conftest for pytest
"""

import pytest
from django.contrib.auth import get_user_model
from categories.models import Category
from products.models import Product

User = get_user_model()


@pytest.fixture
def create_user(db):
    """Fixture to create a test user"""
    def _create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    ):
        return User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
    return _create_user


@pytest.fixture
def create_category(db):
    """Fixture to create a test category"""
    def _create_category(name='Electronics', description='Test category'):
        return Category.objects.create(
            name=name,
            description=description
        )
    return _create_category


@pytest.fixture
def create_product(db, create_category, create_user):
    """Fixture to create a test product"""
    def _create_product(
        name='Test Product',
        sku='TEST-001',
        price='99.99',
        quantity=10,
        category=None,
        created_by=None
    ):
        if not category:
            category = create_category()
        if not created_by:
            created_by = create_user()

        return Product.objects.create(
            name=name,
            sku=sku,
            price=price,
            quantity_in_stock=quantity,
            category=category,
            created_by=created_by,
            description='Test product description',
            image='test.jpg'
        )
    return _create_product


@pytest.fixture
def api_client():
    """Fixture for API client"""
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def authenticated_client(api_client, create_user):
    """Fixture for authenticated API client"""
    user = create_user()
    api_client.force_authenticate(user=user)
    return api_client
