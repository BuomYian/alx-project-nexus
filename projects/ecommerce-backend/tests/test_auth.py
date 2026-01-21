"""
Tests for authentication
"""

import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
class TestAuthentication:
    """Test authentication endpoints"""

    def test_user_registration(self, api_client):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert User.objects.filter(username='newuser').exists()

    def test_user_login(self, api_client, create_user):
        """Test user login"""
        create_user(username='testuser', password='testpass123')
        data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        response = api_client.post('/api/auth/login/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_token_refresh(self, api_client, create_user):
        """Test token refresh"""
        create_user(username='testuser', password='testpass123')
        # First login to get tokens
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass123'
        }
        login_response = api_client.post('/api/auth/login/', login_data, format='json')
        refresh_token = login_response.data['refresh']
        
        # Now refresh the token
        refresh_data = {'refresh': refresh_token}
        response = api_client.post('/api/auth/refresh/', refresh_data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data

    def test_get_user_profile(self, authenticated_client):
        """Test getting user profile"""
        response = authenticated_client.get('/api/auth/users/me/')
        assert response.status_code == status.HTTP_200_OK
        assert 'email' in response.data

    def test_update_user_profile(self, authenticated_client):
        """Test updating user profile"""
        data = {
            'first_name': 'John',
            'last_name': 'Doe'
        }
        response = authenticated_client.put('/api/auth/users/update_profile/', data, format='json')
        assert response.status_code == status.HTTP_200_OK

    def test_password_mismatch_registration(self, api_client):
        """Test registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'testpass123',
            'password2': 'differentpass'
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_duplicate_email_registration(self, api_client, create_user):
        """Test registration with duplicate email"""
        create_user(email='existing@example.com')
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',
            'password': 'testpass123',
            'password2': 'testpass123'
        }
        response = api_client.post('/api/auth/register/', data, format='json')
        assert response.status_code == status.HTTP_400_BAD_REQUEST
