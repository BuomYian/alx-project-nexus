"""
GraphQL schema for interactions.
"""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from interactions.models import PostLike, CommentLike, Share, View, Notification
from posts.models import Post, Comment


class UserType(DjangoObjectType):
    """GraphQL type for User."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')


class PostLikeType(DjangoObjectType):
    """GraphQL type for PostLike."""
    user = graphene.Field(UserType)

    class Meta:
        model = PostLike
        fields = ('id', 'post', 'user', 'created_at')


class CommentLikeType(DjangoObjectType):
    """GraphQL type for CommentLike."""
    user = graphene.Field(UserType)

    class Meta:
        model = CommentLike
        fields = ('id', 'comment', 'user', 'created_at')


class ShareType(DjangoObjectType):
    """GraphQL type for Share."""
    user = graphene.Field(UserType)

    class Meta:
        model = Share
        fields = ('id', 'post', 'user', 'shared_at', 'share_message')


class ViewType(DjangoObjectType):
    """GraphQL type for View."""
    user = graphene.Field(UserType)

    class Meta:
        model = View
        fields = ('id', 'post', 'user', 'viewed_at')


class NotificationType(DjangoObjectType):
    """GraphQL type for Notification."""
    actor = graphene.Field(UserType)
    user = graphene.Field(UserType)

    class Meta:
        model = Notification
        fields = ('id', 'user', 'actor', 'notification_type', 'post', 'comment', 'is_read', 'created_at')


class Query(graphene.ObjectType):
    """Queries for interactions."""
    post_likes = graphene.List(PostLikeType, post_id=graphene.Int())
    comment_likes = graphene.List(CommentLikeType, comment_id=graphene.Int())
    post_shares = graphene.List(ShareType, post_id=graphene.Int())
    post_views = graphene.List(ViewType, post_id=graphene.Int())
    user_notifications = graphene.List(NotificationType)
    unread_notifications_count = graphene.Int()

    def resolve_post_likes(self, info, post_id):
        return PostLike.objects.filter(post_id=post_id).select_related('user')

    def resolve_comment_likes(self, info, comment_id):
        return CommentLike.objects.filter(comment_id=comment_id).select_related('user')

    def resolve_post_shares(self, info, post_id):
        return Share.objects.filter(post_id=post_id).select_related('user')

    def resolve_post_views(self, info, post_id):
        return View.objects.filter(post_id=post_id).select_related('user')

    def resolve_user_notifications(self, info):
        if not info.context.user.is_authenticated:
            return []
        return Notification.objects.filter(user=info.context.user).select_related('actor').order_by('-created_at')[:50]

    def resolve_unread_notifications_count(self, info):
        if not info.context.user.is_authenticated:
            return 0
        return Notification.objects.filter(user=info.context.user, is_read=False).count()


class LikePost(graphene.Mutation):
    """Mutation to like a post."""
    class Arguments:
        post_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    like = graphene.Field(PostLikeType)

    def mutate(self, info, post_id):
        if not info.context.user.is_authenticated:
            return LikePost(success=False, message='User not authenticated')

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return LikePost(success=False, message='Post not found')

        like, created = PostLike.objects.get_or_create(post=post, user=info.context.user)

        if not created:
            return LikePost(success=False, message='Already liked this post')

        return LikePost(like=like, success=True, message='Post liked successfully')


class UnlikePost(graphene.Mutation):
    """Mutation to unlike a post."""
    class Arguments:
        post_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, post_id):
        if not info.context.user.is_authenticated:
            return UnlikePost(success=False, message='User not authenticated')

        try:
            PostLike.objects.get(post_id=post_id, user=info.context.user).delete()
            return UnlikePost(success=True, message='Post unliked successfully')
        except PostLike.DoesNotExist:
            return UnlikePost(success=False, message='You have not liked this post')


class LikeComment(graphene.Mutation):
    """Mutation to like a comment."""
    class Arguments:
        comment_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    like = graphene.Field(CommentLikeType)

    def mutate(self, info, comment_id):
        if not info.context.user.is_authenticated:
            return LikeComment(success=False, message='User not authenticated')

        try:
            comment = Comment.objects.get(pk=comment_id)
        except Comment.DoesNotExist:
            return LikeComment(success=False, message='Comment not found')

        like, created = CommentLike.objects.get_or_create(comment=comment, user=info.context.user)

        if not created:
            return LikeComment(success=False, message='Already liked this comment')

        return LikeComment(like=like, success=True, message='Comment liked successfully')


class SharePost(graphene.Mutation):
    """Mutation to share a post."""
    class Arguments:
        post_id = graphene.Int(required=True)
        share_message = graphene.String()

    success = graphene.Boolean()
    message = graphene.String()
    share = graphene.Field(ShareType)

    def mutate(self, info, post_id, share_message=None):
        if not info.context.user.is_authenticated:
            return SharePost(success=False, message='User not authenticated')

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            return SharePost(success=False, message='Post not found')

        share = Share.objects.create(
            post=post,
            user=info.context.user,
            share_message=share_message
        )

        return SharePost(share=share, success=True, message='Post shared successfully')


class MarkNotificationAsRead(graphene.Mutation):
    """Mutation to mark a notification as read."""
    class Arguments:
        notification_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()
    notification = graphene.Field(NotificationType)

    def mutate(self, info, notification_id):
        if not info.context.user.is_authenticated:
            return MarkNotificationAsRead(success=False, message='User not authenticated')

        try:
            notification = Notification.objects.get(pk=notification_id)
            if notification.user != info.context.user:
                return MarkNotificationAsRead(success=False, message='Permission denied')

            notification.is_read = True
            notification.save()
            return MarkNotificationAsRead(notification=notification, success=True, message='Notification marked as read')
        except Notification.DoesNotExist:
            return MarkNotificationAsRead(success=False, message='Notification not found')


class InteractionMutations(graphene.ObjectType):
    """Interaction mutations."""
    like_post = LikePost.Field()
    unlike_post = UnlikePost.Field()
    like_comment = LikeComment.Field()
    share_post = SharePost.Field()
    mark_notification_as_read = MarkNotificationAsRead.Field()
