"""
Orders Views for ALX Project Nexus E-commerce Backend

This module provides API endpoints for order management and processing.
Includes order creation, tracking, status updates, and order history.
"""

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q, Sum, F
from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import logging

from .models import Order, OrderItem
from .serializers import (
    OrderSerializer,
    OrderListSerializer,
    OrderCreateSerializer,
    OrderUpdateSerializer,
    OrderItemSerializer,
    OrderStatusSerializer
)
from products.models import Product

logger = logging.getLogger(__name__)


class OrderListView(generics.ListCreateAPIView):
    """
    List user's orders or create a new order.
    
    GET: Returns paginated list of user's orders
    POST: Create new order from cart or direct items
    """
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Get orders for current user with related data"""
        return Order.objects.filter(
            user=self.request.user
        ).select_related('user').prefetch_related(
            'items__product', 'items__product__category'
        ).order_by('-created_at')
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.request.method == 'GET':
            return OrderListSerializer
        return OrderCreateSerializer
    
    def list(self, request, *args, **kwargs):
        """List user's orders with filtering"""
        try:
            queryset = self.get_queryset()
            
            # Optional filtering by status
            status_filter = request.query_params.get('status')
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            
            # Optional date range filtering
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'orders': serializer.data,
                'total_count': queryset.count()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error listing orders for user {request.user.email}: {e}")
            return Response({
                'error': 'Unable to retrieve orders'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def create(self, request, *args, **kwargs):
        """Create new order"""
        try:
            with transaction.atomic():
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                order = serializer.save(user=request.user)
                
                logger.info(f"Order created by {request.user.email}: {order.order_number}")
                
                return Response({
                    'message': 'Order created successfully',
                    'order': OrderSerializer(order).data
                }, status=status.HTTP_201_CREATED)
                
        except ValidationError as e:
            logger.warning(f"Order creation validation error: {e}")
            return Response({
                'error': 'Order creation failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Order creation error: {e}")
            return Response({
                'error': 'Order creation failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update, or cancel an order.
    
    GET: Get order details
    PATCH: Update order status (limited updates allowed)
    DELETE: Cancel order (if allowed)
    """
    permission_classes = [IsAuthenticated]
    lookup_field = 'order_number'
    
    def get_queryset(self):
        """Get orders for current user or admin can see all"""
        if self.request.user.is_staff:
            return Order.objects.select_related('user').prefetch_related(
                'items__product', 'items__product__category'
            ).all()
        return Order.objects.filter(
            user=self.request.user
        ).select_related('user').prefetch_related(
            'items__product', 'items__product__category'
        )
    
    def get_serializer_class(self):
        """Use different serializers for different actions"""
        if self.request.method == 'GET':
            return OrderSerializer
        return OrderUpdateSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Get order details"""
        try:
            order = self.get_object()
            serializer = self.get_serializer(order)
            
            return Response({
                'order': serializer.data
            }, status=status.HTTP_200_OK)
            
        except Order.DoesNotExist:
            return Response({
                'error': 'Order not found'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error retrieving order: {e}")
            return Response({
                'error': 'Unable to retrieve order'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def update(self, request, *args, **kwargs):
        """Update order (limited fields allowed)"""
        try:
            order = self.get_object()
            
            # Check if order can be updated
            if order.status in ['delivered', 'cancelled']:
                return Response({
                    'error': 'Cannot update order that is already delivered or cancelled'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Only allow certain fields to be updated
            allowed_fields = ['shipping_address', 'phone_number']
            if request.user.is_staff:
                allowed_fields.extend(['status', 'tracking_number'])
            
            # Filter request data to only allowed fields
            filtered_data = {k: v for k, v in request.data.items() if k in allowed_fields}
            
            serializer = self.get_serializer(order, data=filtered_data, partial=True)
            serializer.is_valid(raise_exception=True)
            updated_order = serializer.save()
            
            logger.info(f"Order updated: {order.order_number} by {request.user.email}")
            
            return Response({
                'message': 'Order updated successfully',
                'order': OrderSerializer(updated_order).data
            }, status=status.HTTP_200_OK)
            
        except ValidationError as e:
            return Response({
                'error': 'Order update failed',
                'details': serializer.errors if 'serializer' in locals() else str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Order update error: {e}")
            return Response({
                'error': 'Order update failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def destroy(self, request, *args, **kwargs):
        """Cancel order (if allowed)"""
        try:
            order = self.get_object()
            
            # Check if order can be cancelled
            if order.status in ['shipped', 'delivered', 'cancelled']:
                return Response({
                    'error': 'Cannot cancel order that is already shipped, delivered, or cancelled'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Only allow user to cancel their own orders, or admin can cancel any
            if not request.user.is_staff and order.user != request.user:
                return Response({
                    'error': 'Permission denied'
                }, status=status.HTTP_403_FORBIDDEN)
            
            with transaction.atomic():
                # Restore stock for all items
                for item in order.items.all():
                    product = item.product
                    product.stock_quantity += item.quantity
                    product.save()
                
                # Update order status
                order.status = 'cancelled'
                order.save()
            
            logger.info(f"Order cancelled: {order.order_number} by {request.user.email}")
            
            return Response({
                'message': 'Order cancelled successfully'
            }, status=status.HTTP_204_NO_CONTENT)
            
        except Exception as e:
            logger.error(f"Order cancellation error: {e}")
            return Response({
                'error': 'Order cancellation failed due to server error'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminOrderListView(generics.ListAPIView):
    """
    Admin view to list all orders with filtering and search.
    
    Only accessible by staff members.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = OrderListSerializer
    
    def get_queryset(self):
        """Get all orders for admin"""
        if not self.request.user.is_staff:
            return Order.objects.none()
        
        return Order.objects.select_related('user').prefetch_related(
            'items__product'
        ).order_by('-created_at')
    
    def list(self, request, *args, **kwargs):
        """List all orders with admin filtering"""
        if not request.user.is_staff:
            return Response({
                'error': 'Permission denied. Admin access required.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        try:
            queryset = self.get_queryset()
            
            # Admin filtering options
            status_filter = request.query_params.get('status')
            user_email = request.query_params.get('user_email')
            date_from = request.query_params.get('date_from')
            date_to = request.query_params.get('date_to')
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            if user_email:
                queryset = queryset.filter(user__email__icontains=user_email)
            if date_from:
                queryset = queryset.filter(created_at__gte=date_from)
            if date_to:
                queryset = queryset.filter(created_at__lte=date_to)
            
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            
            serializer = self.get_serializer(queryset, many=True)
            return Response({
                'orders': serializer.data,
                'total_count': queryset.count()
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Error listing orders for admin: {e}")
            return Response({
                'error': 'Unable to retrieve orders'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status_view(request, order_number):
    """
    Update order status (Admin only).
    
    Allows admin to update order status and tracking information.
    """
    if not request.user.is_staff:
        return Response({
            'error': 'Permission denied. Admin access required.'
        }, status=status.HTTP_403_FORBIDDEN)
    
    try:
        order = Order.objects.get(order_number=order_number)
        
        serializer = OrderStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        updated_order = serializer.save()
        
        logger.info(f"Order status updated: {order.order_number} to {updated_order.status} by {request.user.email}")
        
        return Response({
            'message': 'Order status updated successfully',
            'order': OrderSerializer(updated_order).data
        }, status=status.HTTP_200_OK)
        
    except Order.DoesNotExist:
        return Response({
            'error': 'Order not found'
        }, status=status.HTTP_404_NOT_FOUND)
    except ValidationError as e:
        return Response({
            'error': 'Status update failed',
            'details': serializer.errors if 'serializer' in locals() else str(e)
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Order status update error: {e}")
        return Response({
            'error': 'Status update failed due to server error'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_statistics_view(request):
    """
    Get order statistics for current user or admin.
    
    Returns summary of orders by status, total spent, etc.
    """
    try:
        if request.user.is_staff:
            # Admin gets global statistics
            orders = Order.objects.all()
            user_label = "all users"
        else:
            # Regular user gets their own statistics
            orders = Order.objects.filter(user=request.user)
            user_label = "your"
        
        # Calculate statistics
        total_orders = orders.count()
        total_amount = orders.aggregate(
            total=Sum('total_amount')
        )['total'] or 0
        
        # Orders by status
        status_counts = {}
        for status_choice in Order.STATUS_CHOICES:
            status_key = status_choice[0]
            status_counts[status_key] = orders.filter(status=status_key).count()
        
        # Recent orders (last 30 days)
        recent_date = timezone.now() - timedelta(days=30)
        recent_orders = orders.filter(created_at__gte=recent_date).count()
        
        return Response({
            'statistics': {
                'total_orders': total_orders,
                'total_amount': float(total_amount),
                'status_breakdown': status_counts,
                'recent_orders_30_days': recent_orders,
                'user_scope': user_label
            }
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f"Order statistics error: {e}")
        return Response({
            'error': 'Unable to retrieve order statistics'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_order_view(request, order_number):
    """
    Track order by order number.
    
    Returns order tracking information and status history.
    """
    try:
        # User can track their own orders, admin can track any order
        if request.user.is_staff:
            order = Order.objects.get(order_number=order_number)
        else:
            order = Order.objects.get(order_number=order_number, user=request.user)
        
        # Create tracking timeline based on status
        timeline = []
        if order.status == 'pending':
            timeline.append({
                'status': 'pending',
                'title': 'Order Placed',
                'description': 'Your order has been received and is being processed',
                'completed': True,
                'date': order.created_at
            })
        elif order.status in ['processing', 'shipped', 'delivered']:
            timeline.extend([
                {
                    'status': 'pending',
                    'title': 'Order Placed',
                    'description': 'Your order has been received',
                    'completed': True,
                    'date': order.created_at
                },
                {
                    'status': 'processing',
                    'title': 'Processing',
                    'description': 'Your order is being prepared for shipment',
                    'completed': order.status in ['processing', 'shipped', 'delivered'],
                    'date': order.updated_at if order.status != 'pending' else None
                }
            ])
            
            if order.status in ['shipped', 'delivered']:
                timeline.append({
                    'status': 'shipped',
                    'title': 'Shipped',
                    'description': f'Your order has been shipped{f" - Tracking: {order.tracking_number}" if order.tracking_number else ""}',
                    'completed': True,
                    'date': order.updated_at
                })
            
            if order.status == 'delivered':
                timeline.append({
                    'status': 'delivered',
                    'title': 'Delivered',
                    'description': 'Your order has been delivered successfully',
                    'completed': True,
                    'date': order.updated_at
                })
        elif order.status == 'cancelled':
            timeline.append({
                'status': 'cancelled',
                'title': 'Order Cancelled',
                'description': 'Your order has been cancelled',
                'completed': True,
                'date': order.updated_at
            })
        
        return Response({
            'order': {
                'order_number': order.order_number,
                'status': order.status,
                'tracking_number': order.tracking_number,
                'created_at': order.created_at,
                'updated_at': order.updated_at
            },
            'tracking_timeline': timeline
        }, status=status.HTTP_200_OK)
        
    except Order.DoesNotExist:
        return Response({
            'error': 'Order not found or access denied'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Order tracking error: {e}")
        return Response({
            'error': 'Unable to retrieve order tracking information'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
