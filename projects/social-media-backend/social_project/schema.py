"""
Main GraphQL schema for the social media backend.
"""
import graphene
from users.schema import Query as UserQuery, UserMutations
from posts.schema import Query as PostQuery, PostMutations
from interactions.schema import Query as InteractionQuery, InteractionMutations


class Query(UserQuery, PostQuery, InteractionQuery):
    """Combined queries from all apps."""
    pass


class Mutation(UserMutations, PostMutations, InteractionMutations):
    """Combined mutations from all apps."""
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
