"""
Serializers for reviews app
"""

from rest_framework import serializers
from .models import Review
from accounts.serializers import UserSerializer


class ReviewListSerializer(serializers.ModelSerializer):
    """Serializer for review listing"""
    user_email = serializers.CharField(source='user.email', read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_email', 'rating', 'title', 'comment',
            'is_verified_purchase', 'helpful_count', 'unhelpful_count',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at',
                            'helpful_count', 'unhelpful_count']


class ReviewCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating reviews"""
    class Meta:
        model = Review
        fields = ['rating', 'title', 'comment', 'is_verified_purchase']

    def validate_rating(self, value):
        if not 1 <= value <= 5:
            raise serializers.ValidationError('Rating must be between 1 and 5')
        return value

    def validate_title(self, value):
        if len(value) < 5:
            raise serializers.ValidationError(
                'Title must be at least 5 characters long')
        return value

    def validate_comment(self, value):
        if len(value) < 10:
            raise serializers.ValidationError(
                'Comment must be at least 10 characters long')
        return value
