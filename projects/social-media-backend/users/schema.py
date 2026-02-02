"""
GraphQL schema for users.
"""
import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from users.models import Profile, Follow


class UserType(DjangoObjectType):
    """GraphQL type for User."""
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'date_joined')


class ProfileType(DjangoObjectType):
    """GraphQL type for Profile."""
    followers_count = graphene.Int()
    following_count = graphene.Int()
    posts_count = graphene.Int()
    user = graphene.Field(UserType)

    class Meta:
        model = Profile
        fields = ('id', 'user', 'bio', 'avatar', 'cover_image', 'created_at', 'updated_at')

    def resolve_followers_count(self, info):
        return self.user.followers.count()

    def resolve_following_count(self, info):
        return self.user.following.count()

    def resolve_posts_count(self, info):
        return self.user.posts.count()


class FollowType(DjangoObjectType):
    """GraphQL type for Follow."""
    class Meta:
        model = Follow
        fields = ('id', 'follower', 'following', 'created_at')


class Query(graphene.ObjectType):
    """Queries for users."""
    all_users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())
    user_by_username = graphene.Field(UserType, username=graphene.String())
    user_profile = graphene.Field(ProfileType, user_id=graphene.Int())
    is_following = graphene.Boolean(user_id=graphene.Int())

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_user(self, info, id):
        try:
            return User.objects.get(pk=id)
        except User.DoesNotExist:
            return None

    def resolve_user_by_username(self, info, username):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None

    def resolve_user_profile(self, info, user_id):
        try:
            return Profile.objects.get(user_id=user_id)
        except Profile.DoesNotExist:
            return None

    def resolve_is_following(self, info, user_id):
        if not info.context.user.is_authenticated:
            return False
        try:
            Follow.objects.get(follower=info.context.user, following_id=user_id)
            return True
        except Follow.DoesNotExist:
            return False


class FollowUser(graphene.Mutation):
    """Mutation to follow a user."""
    class Arguments:
        user_id = graphene.Int(required=True)

    user = graphene.Field(UserType)
    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, user_id):
        if not info.context.user.is_authenticated:
            return FollowUser(success=False, message='User not authenticated')

        try:
            user_to_follow = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return FollowUser(success=False, message='User not found')

        if info.context.user == user_to_follow:
            return FollowUser(success=False, message='Cannot follow yourself')

        follow, created = Follow.objects.get_or_create(
            follower=info.context.user,
            following=user_to_follow
        )

        if not created:
            return FollowUser(success=False, message='Already following this user')

        return FollowUser(success=True, user=user_to_follow, message='Successfully followed')


class UnfollowUser(graphene.Mutation):
    """Mutation to unfollow a user."""
    class Arguments:
        user_id = graphene.Int(required=True)

    success = graphene.Boolean()
    message = graphene.String()

    def mutate(self, info, user_id):
        if not info.context.user.is_authenticated:
            return UnfollowUser(success=False, message='User not authenticated')

        try:
            Follow.objects.get(follower=info.context.user, following_id=user_id).delete()
            return UnfollowUser(success=True, message='Successfully unfollowed')
        except Follow.DoesNotExist:
            return UnfollowUser(success=False, message='Not following this user')


class UserMutations(graphene.ObjectType):
    """User mutations."""
    follow_user = FollowUser.Field()
    unfollow_user = UnfollowUser.Field()
