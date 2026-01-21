"""
Views/ViewSets for products app
"""

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Product
from .serializers import (
    ProductListSerializer,
    ProductDetailSerializer,
    ProductCreateUpdateSerializer
)
from .filters import ProductFilter


class ProductViewSet(viewsets.ModelViewSet):
    """ViewSet for product CRUD operations with advanced filtering and pagination"""
    queryset = Product.objects.filter(is_active=True)
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description', 'sku']
    ordering_fields = ['price', 'created_at', 'sales_count', 'average_rating']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ProductCreateUpdateSerializer
        return ProductListSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        
        # Include inactive products for staff
        if self.request.user and self.request.user.is_staff:
            queryset = Product.objects.all()
        
        # Optimize queries
        return queryset.select_related('category').prefetch_related('attributes')

    def perform_create(self, serializer):
        """Create product with current user as creator"""
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def increment_sales(self, request, pk=None):
        """Increment product sales count"""
        product = self.get_object()
        product.sales_count += 1
        product.save(update_fields=['sales_count'])
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def featured(self, request):
        """Get featured products"""
        products = self.get_queryset().filter(is_featured=True).order_by('-sales_count')[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def best_sellers(self, request):
        """Get best selling products"""
        products = self.get_queryset().order_by('-sales_count')[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def top_rated(self, request):
        """Get top rated products"""
        products = self.get_queryset().order_by('-average_rating')[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticatedOrReadOnly])
    def latest(self, request):
        """Get latest products"""
        products = self.get_queryset().order_by('-created_at')[:10]
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
