"""
GraphQL schema for posts.
"""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from posts.models import Post, Comment, Hashtag, Mention
from utils.caching import cache_result, get_cached_or_fetch
from django.core.cache import cache


class UserType(DjangoObjectType):
    """GraphQL type for User."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class HashtagType(DjangoObjectType):
    """GraphQL type for Hashtag."""
    post_count = graphene.Int()

    class Meta:
        model = Hashtag
        fields = ('id', 'tag', 'created_at')

    def resolve_post_count(self, info):
        return self.posts.count()


class MentionType(DjangoObjectType):
    """GraphQL type for Mention."""
    mentioned_user = graphene.Field(UserType)

    class Meta:
        model = Mention
        fields = ('id', 'post', 'mentioned_user', 'created_at')


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
    hashtags = graphene.List(HashtagType)
    mentions = graphene.List(MentionType)

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

    def resolve_hashtags(self, info):
        return self.hashtags.all()

    def resolve_mentions(self, info):
        return self.mentions.all()


class Query(graphene.ObjectType):
    """Queries for posts."""
    all_posts = graphene.List(PostType)
    post = graphene.Field(PostType, id=graphene.Int())
    user_posts = graphene.List(PostType, user_id=graphene.Int())
    search_posts = graphene.List(PostType, query=graphene.String())
    search_posts_fts = graphene.List(PostType, query=graphene.String())
    trending_posts = graphene.List(PostType, limit=graphene.Int())
    hashtag_posts = graphene.List(PostType, tag=graphene.String())
    hashtags = graphene.List(HashtagType, limit=graphene.Int())
    trending_hashtags = graphene.List(HashtagType, limit=graphene.Int())
    user_mentions = graphene.List(MentionType, user_id=graphene.Int())

    def resolve_all_posts(self, info, **kwargs):
        cache_key = 'all_posts:published'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        posts = Post.objects.filter(is_published=True).select_related('author').prefetch_related('likes', 'comments', 'hashtags')
        cache.set(cache_key, list(posts), 300)
        return posts

    def resolve_post(self, info, id):
        try:
            cache_key = f'post:{id}'
            cached = cache.get(cache_key)
            if cached:
                return cached
            
            post = Post.objects.select_related('author').prefetch_related('likes', 'comments', 'hashtags', 'mentions').get(pk=id)
            cache.set(cache_key, post, 300)
            return post
        except Post.DoesNotExist:
            return None

    def resolve_user_posts(self, info, user_id):
        return Post.objects.filter(author_id=user_id, is_published=True).select_related('author')

    def resolve_search_posts(self, info, query):
        """Basic substring search."""
        return Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        ).select_related('author')

    def resolve_search_posts_fts(self, info, query):
        """Full-text search using PostgreSQL FTS."""
        cache_key = f'fts_search:{query}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            search_query = SearchQuery(query, search_type='websearch')
            search_vector = SearchVector('title', weight='A') + SearchVector('content', weight='B')
            posts = Post.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(
                rank__gt=0,
                is_published=True
            ).order_by('-rank').select_related('author')
            
            posts_list = list(posts)
            cache.set(cache_key, posts_list, 600)
            return posts_list
        except Exception:
            # Fallback to basic search if FTS fails
            return info.context.resolve_search_posts(info, query)

    def resolve_trending_posts(self, info, limit=10):
        from django.db.models import Count
        return Post.objects.filter(is_published=True).annotate(
            like_count=Count('likes')
        ).order_by('-like_count')[:limit]

    def resolve_hashtag_posts(self, info, tag):
        """Get posts for a specific hashtag."""
        cache_key = f'hashtag_posts:{tag}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        try:
            hashtag = Hashtag.objects.get(tag__iexact=tag)
            posts = hashtag.posts.filter(is_published=True).select_related('author')
            posts_list = list(posts)
            cache.set(cache_key, posts_list, 300)
            return posts_list
        except Hashtag.DoesNotExist:
            return []

    def resolve_hashtags(self, info, limit=20):
        """Get all hashtags."""
        cache_key = f'hashtags:all:{limit}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        hashtags = Hashtag.objects.all().order_by('-created_at')[:limit]
        hashtags_list = list(hashtags)
        cache.set(cache_key, hashtags_list, 600)
        return hashtags_list

    def resolve_trending_hashtags(self, info, limit=10):
        """Get trending hashtags by post count."""
        cache_key = f'trending_hashtags:{limit}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        from django.db.models import Count
        hashtags = Hashtag.objects.annotate(
            post_count=Count('posts')
        ).order_by('-post_count')[:limit]
        hashtags_list = list(hashtags)
        cache.set(cache_key, hashtags_list, 600)
        return hashtags_list

    def resolve_user_mentions(self, info, user_id):
        """Get mentions for a specific user."""
        cache_key = f'user_mentions:{user_id}'
        cached = cache.get(cache_key)
        if cached:
            return cached
        
        mentions = Mention.objects.filter(mentioned_user_id=user_id).select_related('post', 'mentioned_user')
        mentions_list = list(mentions)
        cache.set(cache_key, mentions_list, 300)
        return mentions_list



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
        
        # Extract and save hashtags
        post.extract_hashtags()
        
        # Extract and save mentions
        post.extract_mentions()
        
        # Invalidate cache
        cache.delete('all_posts:published')
        
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
            
            # Re-extract hashtags and mentions
            post.hashtags.clear()
            post.mentions.all().delete()
            post.extract_hashtags()
            post.extract_mentions()
            
            # Invalidate cache
            cache.delete(f'post:{id}')
            cache.delete('all_posts:published')
            
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
            
            # Invalidate cache
            cache.delete(f'post:{id}')
            cache.delete('all_posts:published')
            
            return DeletePost(success=True, message='Post deleted successfully')
        except Post.DoesNotExist:
            return DeletePost(success=False, message='Post not found')



class PostMutations(graphene.ObjectType):
    """Post mutations."""
    create_post = CreatePost.Field()
    update_post = UpdatePost.Field()
    delete_post = DeletePost.Field()
