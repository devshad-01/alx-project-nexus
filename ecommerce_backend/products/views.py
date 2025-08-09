"""
Products Views for ALX Project Nexus E-commerce Backend

This module provides API endpoints for product and category management.
Includes CRUD operations, filtering, searching, and pagination.
"""

from rest_framework import generics, status, permissions, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Avg, Count
from django.core.exceptions import ValidationError
from django.db import transaction
import logging

from drf_spectacular.utils import extend_schema, OpenApiExample, OpenApiResponse, OpenApiParameter
from drf_spectacular.openapi import OpenApiTypes

from .models import Category, Product, ProductImage, Review
from .serializers import (
    CategorySerializer,
    CategoryDetailSerializer,
    ProductSerializer,
    ProductListSerializer,
    ProductCreateSerializer,
    ProductUpdateSerializer,
    ProductImageSerializer,
    ReviewSerializer
)

logger = logging.getLogger(__name__)


class CategoryListView(generics.ListCreateAPIView):
    """
    List all categories or create a new category.
    
    GET: Returns all categories (public access)
    POST: Create new category (admin only)
    """
    queryset = Category.objects.filter(is_active=True).order_by('name')
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @extend_schema(
        summary='List Categories',
        description='''
        Get all active product categories.
        
        **Public Endpoint**: No authentication required for viewing categories.
        
        Categories are returned with their product counts and hierarchical information.
        ''',
        responses={
            200: OpenApiResponse(
                description='List of categories',
                examples=[
                    OpenApiExample(
                        'Categories List',
                        value=[
                            {
                                'id': 1,
                                'name': 'Electronics',
                                'description': 'Electronic devices and gadgets',
                                'slug': 'electronics',
                                'is_active': True,
                                'product_count': 25,
                                'created_at': '2025-08-09T10:00:00Z'
                            },
                            {
                                'id': 2,
                                'name': 'Clothing',
                                'description': 'Fashion and apparel',
                                'slug': 'clothing',
                                'is_active': True,
                                'product_count': 150,
                                'created_at': '2025-08-09T10:00:00Z'
                            }
                        ]
                    )
                ]
            )
        }
    )
    def get(self, request, *args, **kwargs):
        """List all categories"""
        return super().get(request, *args, **kwargs)
    
    @extend_schema(
        summary='Create Category',
        description='''
        Create a new product category.
        
        **Admin Only**: Requires admin authentication.
        ''',
        examples=[
            OpenApiExample(
                'Create Category',
                value={
                    'name': 'Home & Garden',
                    'description': 'Home improvement and garden supplies',
                    'is_active': True
                },
                request_only=True,
            ),
        ],
        responses={
            201: OpenApiResponse(
                description='Category created successfully',
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            'id': 3,
                            'name': 'Home & Garden',
                            'description': 'Home improvement and garden supplies',
                            'slug': 'home-garden',
                            'is_active': True,
                            'product_count': 0,
                            'created_at': '2025-08-09T10:30:00Z'
                        }
                    )
                ]
            ),
            403: OpenApiResponse(
                description='Permission denied - Admin access required'
            )
        }
    )
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.request.method == 'GET':
            return CategoryDetailSerializer
        return CategorySerializer
    
    def create(self, request, *args, **kwargs):
        """Create new category (admin only)"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            category = serializer.save()
            
            logger.info(f"Category created by {request.user.email}: {category.name}")
            
            return Response({
                'message': 'Category created successfully',
                'category': CategoryDetailSerializer(category).data
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            logger.warning(f"Category creation validation error: {e}")
            return Response({
                'error': 'Category creation failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Category creation error: {e}")
            return Response({
                'error': 'Category creation failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a category.
    
    GET: Get category details (public access)
    PUT/PATCH: Update category (admin only)
    DELETE: Delete category (admin only)
    """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategoryDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def update(self, request, *args, **kwargs):
        """Update category (admin only)"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            category = self.get_object()
            serializer = CategorySerializer(category, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_category = serializer.save()
            
            logger.info(f"Category updated by {request.user.email}: {category.name}")
            
            return Response({
                'message': 'Category updated successfully',
                'category': CategoryDetailSerializer(updated_category).data
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({
                'error': 'Category update failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Category update error: {e}")
            return Response({
                'error': 'Category update failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete category (admin only)"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            category = self.get_object()
            
            # Soft delete by setting is_active to False
            category.is_active = False
            category.save()
            
            logger.info(f"Category deleted by {request.user.email}: {category.name}")
            
            return Response({
                'message': 'Category deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            logger.error(f"Category deletion error: {e}")
            return Response({
                'error': 'Category deletion failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductListView(generics.ListCreateAPIView):
    """
    List all products or create a new product.
    
    GET: Returns paginated list of products with filtering and search
    POST: Create new product (admin only)
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_active', 'price']
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['name', 'price', 'created_at', 'stock_quantity']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Get products with related data for optimization"""
        return Product.objects.select_related('category').prefetch_related(
            'images', 'reviews'
        ).filter(is_active=True).annotate(
            annotated_avg_rating=Avg('reviews__rating'),
            annotated_review_count=Count('reviews')
        )
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.request.method == 'GET':
            return ProductListSerializer
        return ProductCreateSerializer
    
    def list(self, request, *args, **kwargs):
        """List products with filtering and pagination"""
        try:
            # Apply filtering and pagination
            queryset = self.filter_queryset(self.get_queryset())
            
            # Additional custom filtering
            min_price = request.query_params.get('min_price')
            max_price = request.query_params.get('max_price')
            min_rating = request.query_params.get('min_rating')
            
            if min_price:
                queryset = queryset.filter(price__gte=min_price)
            if max_price:
                queryset = queryset.filter(price__lte=max_price)
            if min_rating:
                queryset = queryset.filter(annotated_avg_rating__gte=min_rating)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'products': serializer.data,
                'total_count': queryset.count()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error listing products: {e}")
            return Response({
                'error': 'Unable to retrieve products'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        """Create new product (admin only)"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                product = serializer.save()
                
                logger.info(f"Product created by {request.user.email}: {product.name}")
                
                return Response({
                    'message': 'Product created successfully',
                    'product': ProductSerializer(product).data
                }, status=status.HTTP_201_CREATED)
                
        except ValidationError as e:
            logger.warning(f"Product creation validation error: {e}")
            return Response({
                'error': 'Product creation failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Product creation error: {e}")
            return Response({
                'error': 'Product creation failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or delete a product.
    
    GET: Get product details with reviews (public access)
    PUT/PATCH: Update product (admin only)
    DELETE: Delete product (admin only)
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_queryset(self):
        """Get products with all related data"""
        return Product.objects.select_related('category').prefetch_related(
            'images', 'reviews__user'
        ).filter(is_active=True).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        )
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.request.method == 'GET':
            return ProductSerializer
        return ProductUpdateSerializer
    
    def update(self, request, *args, **kwargs):
        """Update product (admin only)"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = self.get_object()
            serializer = self.get_serializer(product, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_product = serializer.save()
            
            logger.info(f"Product updated by {request.user.email}: {product.name}")
            
            return Response({
                'message': 'Product updated successfully',
                'product': ProductSerializer(updated_product).data
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({
                'error': 'Product update failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Product update error: {e}")
            return Response({
                'error': 'Product update failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        """Soft delete product (admin only)"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            product = self.get_object()
            
            # Soft delete by setting is_active to False
            product.is_active = False
            product.save()
            
            logger.info(f"Product deleted by {request.user.email}: {product.name}")
            
            return Response({
                'message': 'Product deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            logger.error(f"Product deletion error: {e}")
            return Response({
                'error': 'Product deletion failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProductReviewListView(generics.ListCreateAPIView):
    """
    List reviews for a product or create a new review.
    
    GET: List all reviews for a product (public access)
    POST: Create new review (authenticated users only)
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        """Get reviews for specific product"""
        product_slug = self.kwargs['product_slug']
        return Review.objects.filter(
            product__slug=product_slug,
            product__is_active=True
        ).select_related('user', 'product').order_by('-created_at')
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.request.method == 'GET':
            return ReviewSerializer
        return ReviewSerializer
    
    def create(self, request, *args, **kwargs):
        """Create new review for product"""
        try:
            product_slug = self.kwargs['product_slug']
            
            # Check if product exists
            try:
                product = Product.objects.get(slug=product_slug, is_active=True)
            except Product.DoesNotExist:
                return Response({
                    'error': 'Product not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if user already reviewed this product
            if Review.objects.filter(product=product, user=request.user).exists():
                return Response({
                    'error': 'You have already reviewed this product'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create review
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            review = serializer.save(user=request.user, product=product)
            
            logger.info(f"Review created by {request.user.email} for product {product.name}")
            
            return Response({
                'message': 'Review created successfully',
                'review': ReviewSerializer(review).data
            }, status=status.HTTP_201_CREATED)
            
        except ValidationError as e:
            return Response({
                'error': 'Review creation failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Review creation error: {e}")
            return Response({
                'error': 'Review creation failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def product_search_view(request):
    """
    Advanced product search endpoint.
    
    Supports full-text search across product name, description, and category.
    """
    try:
        query = request.query_params.get('q', '').strip()
        
        if not query:
            return Response({
                'error': 'Search query parameter "q" is required'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Perform search across multiple fields
        products = Product.objects.select_related('category').prefetch_related(
            'images'
        ).filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query),
            is_active=True
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).order_by('-created_at')
        
        # Apply pagination
        from rest_framework.pagination import PageNumberPagination
        paginator = PageNumberPagination()
        paginator.page_size = 20
        page = paginator.paginate_queryset(products, request)
        
        if page is not None:
            serializer = ProductListSerializer(page, many=True)
            return paginator.get_paginated_response({
                'query': query,
                'results': serializer.data
            })
        
        serializer = ProductListSerializer(products, many=True)
        return Response({
            'query': query,
            'total_results': products.count(),
            'results': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Product search error: {e}")
        return Response({
            'error': 'Search failed due to server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def featured_products_view(request):
    """
    Get featured products.
    
    Returns products marked as featured or top-rated products.
    """
    try:
        # Get featured products (you can add a featured field to Product model)
        # For now, get highest rated products
        featured_products = Product.objects.select_related('category').prefetch_related(
            'images'
        ).filter(
            is_active=True,
            stock_quantity__gt=0
        ).annotate(
            avg_rating=Avg('reviews__rating'),
            review_count=Count('reviews')
        ).order_by('-avg_rating', '-review_count')[:12]
        
        serializer = ProductListSerializer(featured_products, many=True)
        
        return Response({
            'featured_products': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Featured products error: {e}")
        return Response({
            'error': 'Unable to retrieve featured products'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
