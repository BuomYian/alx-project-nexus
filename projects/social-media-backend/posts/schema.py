"""
GraphQL schema for posts.
"""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from posts.models import Post, Comment


class UserType(DjangoObjectType):
    """GraphQL type for User."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class CommentType(DjangoObjectType):
    """GraphQL type for Comment."""
    like_count = graphene.Int()
    author = graphene.Field(UserType)
    replies = graphene.List(lambda: CommentType)

    class Meta:
        model = Comment
        fields = ('id', 'post', 'author', 'content', 'parent', 'created_at', 'updated_at', 'is_edited')

    def resolve_like_count(self, info):
        return self.comment_likes.count()

    def resolve_replies(self, info):
        return self.replies.all()


class PostType(DjangoObjectType):
    """GraphQL type for Post."""
    like_count = graphene.Int()
    comment_count = graphene.Int()
    share_count = graphene.Int()
    view_count = graphene.Int()
    author = graphene.Field(UserType)
    comments = graphene.List(CommentType)
    is_liked_by_user = graphene.Boolean()

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'content', 'image', 'created_at', 'updated_at', 'is_published')

    def resolve_like_count(self, info):
        return self.likes.count()

    def resolve_comment_count(self, info):
        return self.comments.count()

    def resolve_share_count(self, info):
        return self.shares.count()

    def resolve_view_count(self, info):
        return self.views.count()

    def resolve_comments(self, info):
        return self.comments.filter(parent__isnull=True).prefetch_related('replies')

    def resolve_is_liked_by_user(self, info):
        if not info.context.user.is_authenticated:
            return False
        return self.likes.filter(user=info.context.user).exists()


class Query(graphene.ObjectType):
    """Queries for posts."""
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())
    user_posts = graphene.List(PostType, user_id=graphene.Int())
    search_posts = graphene.List(PostType, query=graphene.String())
    trending_posts = graphene.List(PostType, limit=graphene.Int())

    def resolve_all_posts(self, info, **kwargs):
        return Post.objects.filter(is_published=True).select_related('author').prefetch_related('likes', 'comments')

    def resolve_post(self, info, id):
        try:
            return Post.objects.select_related('author').prefetch_related('likes', 'comments').get(pk=id)
        except Post.DoesNotExist:
            return None

    def resolve_user_posts(self, info, user_id):
        return Post.objects.filter(author_id=user_id, is_published=True).select_related('author')

    def resolve_search_posts(self, info, query):
        return Post.objects.filter(
            title__icontains=query,
            is_published=True
        ).select_related('author')

    def resolve_trending_posts(self, info, limit=10):
        from django.db.models import Count
        return Post.objects.filter(is_published=True).annotate(
            like_count=Count('likes')
        ).order_by('-like_count')[:limit]


class CreatePost(graphene.Mutation):
    """Mutation to create a post."""
    class Arguments:
        title = graphene.String(required=True)
        content = graphene.String(required=True)

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, title, content):
        if not info.context.user.is_authenticated:
            return CreatePost(success=False, message='User not authenticated')

        post = Post.objects.create(
            author=info.context.user,
            title=title,
            content=content
        )
        return CreatePost(post=post, success=True, message='Post created successfully')


class UpdatePost(graphene.Mutation):
    """Mutation to update a post."""
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        content = graphene.String()

    post = graphene.Field(PostType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id, title=None, content=None):
        if not info.context.user.is_authenticated:
            return UpdatePost(success=False, message='User not authenticated')

        try:
            post = Post.objects.get(pk=id)
            if post.author != info.context.user:
                return UpdatePost(success=False, message='You can only edit your own posts')

            if title:
                post.title = title
            if content:
                post.content = content
            post.save()
            return UpdatePost(post=post, success=True, message='Post updated successfully')
        except Post.DoesNotExist:
            return UpdatePost(success=False, message='Post not found')


class DeletePost(graphene.Mutation):
    """Mutation to delete a post."""
    class Arguments:
        id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, id):
        if not info.context.user.is_authenticated:
            return DeletePost(success=False, message='User not authenticated')

        try:
            post = Post.objects.get(pk=id)
            if post.author != info.context.user:
                return DeletePost(success=False, message='You can only delete your own posts')
            post.delete()
            return DeletePost(success=True, message='Post deleted successfully')
        except Post.DoesNotExist:
            return DeletePost(success=False, message='Post not found')


class PostMutations(graphene.ObjectType):
    """Post mutations."""
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
