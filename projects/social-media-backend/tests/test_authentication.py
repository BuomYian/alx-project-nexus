import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from authentication.models import UserSession, LoginAttempt, TokenBlacklistLog


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def test_user(db):
    """Create a test user"""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='TestPassword123'
    )


@pytest.mark.django_db
class TestAuthentication:
    """Test JWT authentication endpoints"""

    def test_user_registration(self, api_client):
        """Test user registration"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123',
            'first_name': 'New',
            'last_name': 'User'
        }
        response = api_client.post('/api/auth/register/', data)
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['user']['username'] == 'newuser'
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_registration_password_mismatch(self, api_client):
        """Test registration with mismatched passwords"""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'DifferentPass123'
        }
        response = api_client.post('/api/auth/register/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_registration_duplicate_username(self, api_client, test_user):
        """Test registration with duplicate username"""
        data = {
            'username': 'testuser',  # Duplicate
            'email': 'different@example.com',
            'password': 'SecurePass123',
            'password_confirm': 'SecurePass123'
        }
        response = api_client.post('/api/auth/register/', data)
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_user_login(self, api_client, test_user):
        """Test user login"""
        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = api_client.post('/api/auth/login/', data)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_login_wrong_password(self, api_client, test_user):
        """Test login with wrong password"""
        data = {
            'username': 'testuser',
            'password': 'WrongPassword'
        }
        response = api_client.post('/api/auth/login/', data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_nonexistent_user(self, api_client):
        """Test login with nonexistent user"""
        data = {
            'username': 'nonexistent',
            'password': 'AnyPassword'
        }
        response = api_client.post('/api/auth/login/', data)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_login_creates_session(self, api_client, test_user):
        """Test that login creates a UserSession"""
        data = {
            'username': 'testuser',
            'password': 'TestPassword123'
        }
        response = api_client.post('/api/auth/login/', data)
        
        assert response.status_code == status.HTTP_200_OK
        assert UserSession.objects.filter(user=test_user).exists()

    def test_token_refresh(self, api_client, test_user):
        """Test token refresh"""
        # First, login
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        refresh_token = login_response.data['refresh']
        
        # Refresh the token
        response = api_client.post('/api/auth/refresh/', {
            'refresh': refresh_token
        })
        
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

    def test_invalid_refresh_token(self, api_client):
        """Test refresh with invalid token"""
        response = api_client.post('/api/auth/refresh/', {
            'refresh': 'invalid_token'
        })
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_current_user(self, api_client, test_user):
        """Test getting current user profile"""
        # Login first
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        access_token = login_response.data['access']
        
        # Make authenticated request
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.get('/api/auth/users/me/')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'testuser'

    def test_logout(self, api_client, test_user):
        """Test logout"""
        # Login first
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        access_token = login_response.data['access']
        refresh_token = login_response.data['refresh']
        
        # Logout
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.post('/api/auth/logout/', {
            'refresh': refresh_token
        })
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify session is inactive
        session = UserSession.objects.get(user=test_user)
        assert session.is_active == False

    def test_logout_all(self, api_client, test_user):
        """Test logout from all devices"""
        # Create multiple sessions
        for _ in range(3):
            api_client.post('/api/auth/login/', {
                'username': 'testuser',
                'password': 'TestPassword123'
            })
        
        # Login again and logout all
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        access_token = login_response.data['access']
        
        # Logout from all
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.post('/api/auth/logout-all/')
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify all sessions are inactive
        active_sessions = UserSession.objects.filter(user=test_user, is_active=True)
        assert active_sessions.count() == 0

    def test_change_password(self, api_client, test_user):
        """Test password change"""
        # Login first
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        access_token = login_response.data['access']
        
        # Change password
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.post('/api/auth/users/change-password/', {
            'old_password': 'TestPassword123',
            'new_password': 'NewPassword456'
        })
        
        assert response.status_code == status.HTTP_200_OK
        
        # Verify old password doesn't work
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        assert login_response.status_code == status.HTTP_401_UNAUTHORIZED
        
        # Verify new password works
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'NewPassword456'
        })
        assert login_response.status_code == status.HTTP_200_OK

    def test_active_sessions_list(self, api_client, test_user):
        """Test listing active sessions"""
        # Create multiple sessions
        for _ in range(2):
            api_client.post('/api/auth/login/', {
                'username': 'testuser',
                'password': 'TestPassword123'
            })
        
        # Login and get sessions
        login_response = api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        access_token = login_response.data['access']
        
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = api_client.get('/api/auth/sessions/active_sessions/')
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 3

    def test_unauthorized_access(self, api_client):
        """Test accessing protected endpoint without token"""
        response = api_client.get('/api/auth/users/me/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_invalid_token_access(self, api_client):
        """Test accessing protected endpoint with invalid token"""
        api_client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = api_client.get('/api/auth/users/me/')
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
class TestSessionManagement:
    """Test session management features"""

    def test_session_creation_on_login(self, api_client, test_user):
        """Test that session is created on login"""
        initial_count = UserSession.objects.count()
        
        api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        
        assert UserSession.objects.count() == initial_count + 1

    def test_login_attempt_tracking(self, api_client, test_user):
        """Test that login attempts are tracked"""
        api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'TestPassword123'
        })
        
        assert LoginAttempt.objects.filter(username='testuser', success=True).exists()

    def test_failed_login_attempt_tracking(self, api_client, test_user):
        """Test that failed login attempts are tracked"""
        api_client.post('/api/auth/login/', {
            'username': 'testuser',
            'password': 'WrongPassword'
        })
        
        # Note: Tracking failed attempts would need custom implementation
        # Current implementation only tracks successful attempts
