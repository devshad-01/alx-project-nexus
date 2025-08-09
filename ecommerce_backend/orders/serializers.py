"""
Orders serializers for ALX Project Nexus E-Commerce Backend
Handles order creation, management, and order items
"""

from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from django.utils import timezone
from .models import Order, OrderItem
from products.models import Product
from products.serializers import ProductListSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for order items
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    product_details = ProductListSerializer(source='product', read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'product_name', 'product_sku', 'product_details',
            'quantity', 'unit_price', 'total_price', 'created_at'
        ]
        read_only_fields = ['id', 'unit_price', 'total_price', 'created_at']

    def get_total_price(self, obj):
        """
        Calculate total price for this order item
        """
        return obj.quantity * obj.unit_price

    def validate_quantity(self, value):
        """
        Validate quantity is positive
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_product(self, value):
        """
        Validate product is active and in stock
        """
        if not value.is_active:
            raise serializers.ValidationError("This product is not available.")
        
        return value


class OrderCreateItemSerializer(serializers.Serializer):
    """
    Serializer for creating order items during order creation
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        """
        Validate product exists and is active
        """
        try:
            product = Product.objects.get(id=value, is_active=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product not found or not available.")
        return value

    def validate(self, attrs):
        """
        Validate stock availability
        """
        product_id = attrs['product_id']
        quantity = attrs['quantity']
        
        try:
            product = Product.objects.get(id=product_id)
            if product.stock_quantity < quantity:
                raise serializers.ValidationError({
                    'quantity': f'Only {product.stock_quantity} items available in stock.'
                })
        except Product.DoesNotExist:
            pass  # Will be caught by product_id validation
        
        return attrs


class OrderSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for orders
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_name', 'user_email', 'order_number',
            'status', 'status_display', 'total_amount', 'total_items',
            'shipping_address', 'billing_address', 'payment_method',
            'payment_status', 'notes', 'order_items',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'user_name', 'user_email', 'order_number',
            'total_amount', 'total_items', 'order_items',
            'created_at', 'updated_at'
        ]

    def get_total_items(self, obj):
        """
        Get total number of items in order
        """
        return sum(item.quantity for item in obj.order_items.all())


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new orders
    """
    items = OrderCreateItemSerializer(many=True, write_only=True)
    order_items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'shipping_address', 'billing_address',
            'payment_method', 'notes', 'items', 'order_items',
            'total_amount', 'status', 'created_at'
        ]
        read_only_fields = [
            'id', 'order_number', 'total_amount', 'status', 
            'order_items', 'created_at'
        ]

    def validate_items(self, value):
        """
        Validate order has at least one item
        """
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        
        # Check for duplicate products
        product_ids = [item['product_id'] for item in value]
        if len(product_ids) != len(set(product_ids)):
            raise serializers.ValidationError("Duplicate products in order items.")
        
        return value

    def validate_shipping_address(self, value):
        """
        Validate shipping address has required fields
        """
        required_fields = ['street', 'city', 'country']
        for field in required_fields:
            if not value.get(field):
                raise serializers.ValidationError(
                    f"Shipping address must include {field}."
                )
        return value

    @transaction.atomic
    def create(self, validated_data):
        """
        Create order with items and calculate total
        """
        items_data = validated_data.pop('items')
        
        # Set user from request context
        validated_data['user'] = self.context['request'].user
        
        # Create order
        order = Order.objects.create(**validated_data)
        
        total_amount = Decimal('0.00')
        
        # Create order items
        for item_data in items_data:
            product = Product.objects.get(id=item_data['product_id'])
            quantity = item_data['quantity']
            
            # Check stock availability again (race condition protection)
            if product.stock_quantity < quantity:
                raise serializers.ValidationError({
                    'items': f'Insufficient stock for {product.name}. Only {product.stock_quantity} available.'
                })
            
            # Create order item
            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price
            )
            
            # Update product stock
            product.stock_quantity -= quantity
            product.save()
            
            # Add to total
            total_amount += order_item.quantity * order_item.unit_price
        
        # Update order total
        order.total_amount = total_amount
        order.save()
        
        return order


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating order status and details
    """
    
    class Meta:
        model = Order
        fields = [
            'status', 'shipping_address', 'billing_address',
            'payment_method', 'payment_status', 'notes'
        ]

    def validate_status(self, value):
        """
        Validate status transitions
        """
        if self.instance:
            current_status = self.instance.status
            
            # Define valid status transitions
            valid_transitions = {
                'pending': ['confirmed', 'cancelled'],
                'confirmed': ['processing', 'cancelled'],
                'processing': ['shipped', 'cancelled'],
                'shipped': ['delivered'],
                'delivered': [],  # Final status
                'cancelled': []   # Final status
            }
            
            if value != current_status and value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Cannot change status from '{current_status}' to '{value}'."
                )
        
        return value


class OrderListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for order lists
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    total_items = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'user', 'user_name', 'status',
            'status_display', 'total_amount', 'total_items',
            'payment_method', 'created_at'
        ]

    def get_total_items(self, obj):
        """
        Get total number of items in order
        """
        return sum(item.quantity for item in obj.order_items.all())


class OrderStatusSerializer(serializers.ModelSerializer):
    """
    Serializer for updating only order status
    """
    
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        """
        Validate status transitions
        """
        if self.instance:
            current_status = self.instance.status
            
            # Define valid status transitions
            valid_transitions = {
                'pending': ['confirmed', 'cancelled'],
                'confirmed': ['processing', 'cancelled'],
                'processing': ['shipped', 'cancelled'],
                'shipped': ['delivered'],
                'delivered': [],
                'cancelled': []
            }
            
            if value != current_status and value not in valid_transitions.get(current_status, []):
                raise serializers.ValidationError(
                    f"Cannot change status from '{current_status}' to '{value}'."
                )
        
        return value


class OrderHistorySerializer(serializers.ModelSerializer):
    """
    Serializer for user's order history
    """
    order_items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'status_display',
            'total_amount', 'total_items', 'payment_method',
            'payment_status', 'order_items', 'created_at'
        ]

    def get_total_items(self, obj):
        """
        Get total number of items in order
        """
        return sum(item.quantity for item in obj.order_items.all())
