"""
Core Views for ALX Project Nexus E-commerce Backend

This module provides API endpoints for cart functionality and general utilities.
Includes shopping cart management, wishlist, and other core features.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Sum, F
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
import logging

from .models import Cart, CartItem
from .serializers import (
    CartSerializer,
    CartItemSerializer,
    AddToCartSerializer,
    UpdateCartItemSerializer,
    CartSummarySerializer
)
from products.models import Product

logger = logging.getLogger(__name__)


class CartView(generics.RetrieveAPIView):
    """
    Get current user's cart with all items.
    
    Returns the user's cart with calculated totals and item details.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = CartSerializer
    
    def get_object(self):
        """Get or create cart for current user"""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        if created:
            logger.info(f"New cart created for user: {self.request.user.email}")
        return cart
    
    def retrieve(self, request, *args, **kwargs):
        """Get user's cart"""
        try:
            cart = self.get_object()
            serializer = self.get_serializer(cart)
            
            return Response({
                'cart': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error retrieving cart for user {request.user.email}: {e}")
            return Response({
                'error': 'Unable to retrieve cart'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart_view(request):
    """
    Add item to cart or update quantity if item already exists.
    
    Expects: product_id, quantity
    """
    try:
        with transaction.atomic():
            serializer = AddToCartSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
            
            # Get or create cart
            cart, created = Cart.objects.get_or_create(user=request.user)
            
            # Get product
            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                return Response({
                    'error': 'Product not found or not available'
                }, status=status.HTTP_404_NOT_FOUND)
            
            # Check if product is available
            if not product.is_available:
                return Response({
                    'error': 'Product is not available for purchase'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Get or create cart item
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'quantity': 0}
            )
            
            # Calculate new quantity
            new_quantity = cart_item.quantity + quantity
            
            # Check stock availability
            if new_quantity > product.stock_quantity:
                return Response({
                    'error': f'Insufficient stock. Available: {product.stock_quantity}, Requested: {new_quantity}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update quantity
            cart_item.quantity = new_quantity
            cart_item.save()
            
            # Update cart timestamp
            cart.save()
            
            logger.info(f"Item {'added to' if item_created else 'updated in'} cart for user {request.user.email}: {product.name} x{quantity}")
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            
            return Response({
                'message': f'{"Added to cart" if item_created else "Cart updated"}',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
    except ValidationError as e:
        return Response({
            'error': 'Add to cart failed',
            'details': serializer.errors if 'serializer' in locals() else str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Add to cart error: {e}")
        return Response({
            'error': 'Add to cart failed due to server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_cart_item_view(request, item_id):
    """
    Update quantity of specific cart item.
    
    Expects: quantity
    """
    try:
        with transaction.atomic():
            # Get cart item
            try:
                cart_item = CartItem.objects.select_related('cart', 'product').get(
                    id=item_id,
                    cart__user=request.user
                )
            except CartItem.DoesNotExist:
                return Response({
                    'error': 'Cart item not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            serializer = UpdateCartItemSerializer(cart_item, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            new_quantity = serializer.validated_data['quantity']
            
            # Check stock availability
            if new_quantity > cart_item.product.stock_quantity:
                return Response({
                    'error': f'Insufficient stock. Available: {cart_item.product.stock_quantity}'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Update or remove item
            if new_quantity <= 0:
                product_name = cart_item.product.name
                cart_item.delete()
                message = f'Removed {product_name} from cart'
            else:
                cart_item.quantity = new_quantity
                cart_item.save()
                message = 'Cart item updated'
            
            # Update cart timestamp
            cart_item.cart.save()
            
            logger.info(f"Cart item updated for user {request.user.email}: {message}")
            
            # Return updated cart
            cart_serializer = CartSerializer(cart_item.cart)
            
            return Response({
                'message': message,
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
    except ValidationError as e:
        return Response({
            'error': 'Cart update failed',
            'details': serializer.errors if 'serializer' in locals() else str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Cart update error: {e}")
        return Response({
            'error': 'Cart update failed due to server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart_view(request, item_id):
    """
    Remove specific item from cart.
    """
    try:
        with transaction.atomic():
            # Get cart item
            try:
                cart_item = CartItem.objects.select_related('cart', 'product').get(
                    id=item_id,
                    cart__user=request.user
                )
            except CartItem.DoesNotExist:
                return Response({
                    'error': 'Cart item not found'
                }, status=status.HTTP_404_NOT_FOUND)
            
            product_name = cart_item.product.name
            cart = cart_item.cart
            cart_item.delete()
            
            # Update cart timestamp
            cart.save()
            
            logger.info(f"Item removed from cart for user {request.user.email}: {product_name}")
            
            # Return updated cart
            cart_serializer = CartSerializer(cart)
            
            return Response({
                'message': f'Removed {product_name} from cart',
                'cart': cart_serializer.data
            }, status=status.HTTP_200_OK)
            
    except Exception as e:
        logger.error(f"Remove from cart error: {e}")
        return Response({
            'error': 'Remove from cart failed due to server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def clear_cart_view(request):
    """
    Clear all items from user's cart.
    """
    try:
        with transaction.atomic():
            # Get user's cart
            try:
                cart = Cart.objects.get(user=request.user)
                item_count = cart.items.count()
                cart.items.all().delete()
                cart.save()
                
                logger.info(f"Cart cleared for user {request.user.email}: {item_count} items removed")
                
                return Response({
                    'message': f'Cart cleared. {item_count} items removed.',
                    'cart': CartSerializer(cart).data
                }, status=status.HTTP_200_OK)
                
            except Cart.DoesNotExist:
                return Response({
                    'message': 'Cart is already empty',
                    'cart': CartSerializer(Cart.objects.create(user=request.user)).data
                }, status=status.HTTP_200_OK)
            
    except Exception as e:
        logger.error(f"Clear cart error: {e}")
        return Response({
            'error': 'Clear cart failed due to server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_summary_view(request):
    """
    Get cart summary with totals and item count.
    
    Useful for cart badges and quick summaries.
    """
    try:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=request.user)
        
        serializer = CartSummarySerializer(cart)
        
        return Response({
            'cart_summary': serializer.data
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Cart summary error: {e}")
        return Response({
            'error': 'Unable to retrieve cart summary'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def checkout_validation_view(request):
    """
    Validate cart before checkout.
    
    Checks stock availability, product availability, and calculates final totals.
    """
    try:
        # Get user's cart
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        if not cart.items.exists():
            return Response({
                'error': 'Cart is empty'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validation_errors = []
        valid_items = []
        total_amount = 0
        
        # Validate each cart item
        for item in cart.items.select_related('product').all():
            product = item.product
            
            # Check if product is still active and available
            if not product.is_active:
                validation_errors.append(f'{product.name} is no longer available')
                continue
            
            if not product.is_available:
                validation_errors.append(f'{product.name} is currently out of stock')
                continue
            
            # Check stock quantity
            if item.quantity > product.stock_quantity:
                validation_errors.append(
                    f'{product.name}: Requested {item.quantity}, Available {product.stock_quantity}'
                )
                continue
            
            # Item is valid
            item_total = product.price * item.quantity
            valid_items.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': item.quantity,
                'unit_price': product.price,
                'total_price': item_total
            })
            total_amount += item_total
        
        if validation_errors:
            return Response({
                'valid': False,
                'errors': validation_errors,
                'valid_items': valid_items,
                'total_amount': total_amount
            }, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({
            'valid': True,
            'valid_items': valid_items,
            'total_amount': total_amount,
            'item_count': len(valid_items),
            'message': 'Cart is valid for checkout'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Checkout validation error: {e}")
        return Response({
            'error': 'Checkout validation failed due to server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Utility views
@api_view(['GET'])
@permission_classes([AllowAny])
def health_check_view(request):
    """
    Simple health check endpoint.
    
    Returns API status and basic information.
    """
    return Response({
        'status': 'healthy',
        'message': 'ALX Project Nexus E-commerce API is running',
        'timestamp': timezone.now()
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_info_view(request):
    """
    API information endpoint.
    
    Returns API version and available endpoints information.
    """
    return Response({
        'api_name': 'ALX Project Nexus E-commerce API',
        'version': '1.0.0',
        'description': 'RESTful API for e-commerce backend with authentication, products, orders, and cart functionality',
        'endpoints': {
            'authentication': '/api/auth/',
            'products': '/api/products/',
            'orders': '/api/orders/',
            'cart': '/api/cart/',
            'admin': '/admin/'
        },
        'documentation': '/api/docs/',
        'status': 'active'
    }, status=status.HTTP_200_OK)
