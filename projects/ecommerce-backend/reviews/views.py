"""
Views/ViewSets for reviews app
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Review
from .serializers import ReviewListSerializer, ReviewCreateUpdateSerializer
from products.models import Product


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet for product reviews"""
    queryset = Review.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateUpdateSerializer
        return ReviewListSerializer

    def get_queryset(self):
        # Filter reviews by product if product_id is in URL
        product_id = self.kwargs.get('product_id')
        if product_id:
            return Review.objects.filter(product_id=product_id).order_by('-created_at')
        return super().get_queryset()

    def perform_create(self, serializer):
        """Create review with current user"""
        product_id = self.kwargs.get('product_id')
        
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise ValidationError({'product': 'Product not found'})

        # Check if user already reviewed this product
        if Review.objects.filter(product=product, user=self.request.user).exists():
            raise ValidationError({'error': 'You have already reviewed this product'})

        serializer.save(product=product, user=self.request.user)

    def perform_update(self, serializer):
        """Only allow users to update their own reviews"""
        review = self.get_object()
        if review.user != self.request.user:
            raise ValidationError({'error': 'You can only update your own reviews'})
        serializer.save()

    def perform_destroy(self, instance):
        """Only allow users to delete their own reviews"""
        if instance.user != self.request.user and not self.request.user.is_staff:
            raise ValidationError({'error': 'You can only delete your own reviews'})
        instance.delete()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_helpful(self, request, pk=None):
        """Mark review as helpful"""
        review = self.get_object()
        review.helpful_count += 1
        review.save(update_fields=['helpful_count'])
        serializer = ReviewListSerializer(review)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def mark_unhelpful(self, request, pk=None):
        """Mark review as unhelpful"""
        review = self.get_object()
        review.unhelpful_count += 1
        review.save(update_fields=['unhelpful_count'])
        serializer = ReviewListSerializer(review)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_rating(self, request):
        """Get reviews filtered by rating"""
        rating = request.query_params.get('rating')
        if not rating:
            return Response(
                {'error': 'Rating parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        reviews = self.get_queryset().filter(rating=rating)
        serializer = self.get_serializer(reviews, many=True)
        return Response(serializer.data)
