"""
Tests for user models and authentication.
"""
import pytest
from django.contrib.auth.models import User
from users.models import Profile, Follow


@pytest.mark.django_db
class TestProfileModel:
    """Test Profile model."""

    def test_profile_created_with_user(self):
        """Test that a profile is created when a user is created."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        assert hasattr(user, 'profile')
        assert user.profile.user == user

    def test_profile_update(self):
        """Test updating a profile."""
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )
        user.profile.bio = 'This is my bio'
        user.profile.save()
        assert user.profile.bio == 'This is my bio'


@pytest.mark.django_db
class TestFollowModel:
    """Test Follow model."""

    @pytest.fixture
    def users(self):
        return [
            User.objects.create_user(f'user{i}', f'user{i}@example.com', 'pass')
            for i in range(3)
        ]

    def test_create_follow(self, users):
        """Test creating a follow relationship."""
        follow = Follow.objects.create(
            follower=users[0],
            following=users[1]
        )
        assert follow.follower == users[0]
        assert follow.following == users[1]

    def test_cannot_follow_same_user(self, users):
        """Test that a unique constraint prevents following twice."""
        Follow.objects.create(
            follower=users[0],
            following=users[1]
        )
        with pytest.raises(Exception):
            Follow.objects.create(
                follower=users[0],
                following=users[1]
            )

    def test_follower_count(self, users):
        """Test follower count."""
        Follow.objects.create(follower=users[0], following=users[1])
        Follow.objects.create(follower=users[2], following=users[1])
        assert users[1].followers.count() == 2

    def test_following_count(self, users):
        """Test following count."""
        Follow.objects.create(follower=users[0], following=users[1])
        Follow.objects.create(follower=users[0], following=users[2])
        assert users[0].following.count() == 2
