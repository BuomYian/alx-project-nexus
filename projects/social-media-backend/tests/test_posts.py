"""
Tests for post models and operations.
"""
import pytest
from django.contrib.auth.models import User
from posts.models import Post, Comment


@pytest.mark.django_db
class TestPostModel:
    """Test Post model."""

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    def test_create_post(self, user):
        """Test creating a post."""
        post = Post.objects.create(
            author=user,
            title='Test Post',
            content='This is test content'
        )
        assert post.author == user
        assert post.title == 'Test Post'
        assert post.is_published is True

    def test_post_str_representation(self, user):
        """Test post string representation."""
        post = Post.objects.create(
            author=user,
            title='Test Post',
            content='Content'
        )
        assert str(post) == 'testuser: Test Post'

    def test_post_like_count_property(self, user):
        """Test post like count property."""
        post = Post.objects.create(
            author=user,
            title='Test',
            content='Content'
        )
        assert post.like_count == 0

    def test_post_comment_count_property(self, user):
        """Test post comment count property."""
        post = Post.objects.create(
            author=user,
            title='Test',
            content='Content'
        )
        assert post.comment_count == 0


@pytest.mark.django_db
class TestCommentModel:
    """Test Comment model."""

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass'
        )

    @pytest.fixture
    def post(self, user):
        return Post.objects.create(
            author=user,
            title='Test Post',
            content='Content'
        )

    def test_create_comment(self, post, user):
        """Test creating a comment."""
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='This is a comment'
        )
        assert comment.post == post
        assert comment.author == user
        assert comment.is_edited is False

    def test_comment_reply(self, post, user):
        """Test creating a reply to a comment."""
        parent_comment = Comment.objects.create(
            post=post,
            author=user,
            content='Parent comment'
        )
        reply = Comment.objects.create(
            post=post,
            author=user,
            content='Reply',
            parent=parent_comment
        )
        assert reply.parent == parent_comment
        assert parent_comment.replies.count() == 1

    def test_comment_like_count(self, post, user):
        """Test comment like count."""
        comment = Comment.objects.create(
            post=post,
            author=user,
            content='Test comment'
        )
        assert comment.like_count == 0
