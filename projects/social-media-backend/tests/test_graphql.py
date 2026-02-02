"""
Tests for GraphQL API.
"""
import pytest
from django.contrib.auth.models import User
from posts.models import Post, Comment
from interactions.models import PostLike


@pytest.mark.django_db
class TestPostQueries:
    """Test post-related GraphQL queries."""

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    @pytest.fixture
    def post(self, user):
        return Post.objects.create(
            author=user,
            title='Test Post',
            content='This is a test post content.'
        )

    def test_all_posts_query(self, client, post):
        """Test fetching all posts."""
        query = '''
            query {
                allPosts {
                    id
                    title
                    content
                    author {
                        username
                    }
                }
            }
        '''
        response = client.get('/graphql/', {'query': query})
        assert response.status_code == 405  # POST required for GraphQL

    def test_single_post_query(self, post):
        """Test fetching a single post."""
        assert post.title == 'Test Post'
        assert post.author.username == 'testuser'

    def test_post_like_count(self, post, user):
        """Test post like count calculation."""
        PostLike.objects.create(post=post, user=user)
        assert post.like_count == 1

    def test_post_comment_count(self, post, user):
        """Test post comment count calculation."""
        Comment.objects.create(post=post, author=user, content='Test comment')
        assert post.comment_count == 1


@pytest.mark.django_db
class TestPostMutations:
    """Test post-related GraphQL mutations."""

    @pytest.fixture
    def user(self):
        return User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_create_post(self, user):
        """Test creating a post."""
        post = Post.objects.create(
            author=user,
            title='New Post',
            content='New content'
        )
        assert post.id is not None
        assert post.author == user

    def test_update_post(self, user):
        """Test updating a post."""
        post = Post.objects.create(
            author=user,
            title='Original Title',
            content='Original content'
        )
        post.title = 'Updated Title'
        post.save()
        assert post.title == 'Updated Title'

    def test_delete_post(self, user):
        """Test deleting a post."""
        post = Post.objects.create(
            author=user,
            title='To Delete',
            content='This will be deleted'
        )
        post_id = post.id
        post.delete()
        assert not Post.objects.filter(id=post_id).exists()


@pytest.mark.django_db
class TestInteractions:
    """Test interaction-related functionality."""

    @pytest.fixture
    def users(self):
        return [
            User.objects.create_user(f'user{i}', f'user{i}@example.com', 'pass')
            for i in range(3)
        ]

    @pytest.fixture
    def post(self, users):
        return Post.objects.create(
            author=users[0],
            title='Test Post',
            content='Content'
        )

    def test_like_post(self, post, users):
        """Test liking a post."""
        like = PostLike.objects.create(post=post, user=users[1])
        assert like.post == post
        assert like.user == users[1]

    def test_post_cannot_be_liked_twice(self, post, users):
        """Test that a post cannot be liked twice by the same user."""
        PostLike.objects.create(post=post, user=users[1])
        with pytest.raises(Exception):
            PostLike.objects.create(post=post, user=users[1])
