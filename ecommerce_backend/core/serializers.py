"""
Core serializers for ALX Project Nexus E-Commerce Backend
Handles shopping cart functionality and shared utilities
"""

from rest_framework import serializers
from decimal import Decimal
from django.db import transaction
from .models import Cart, CartItem
from products.models import Product
from products.serializers import ProductListSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    Serializer for cart items
    """
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    product_sku = serializers.CharField(source='product.sku', read_only=True)
    product_details = ProductListSerializer(source='product', read_only=True)
    total_price = serializers.SerializerMethodField()
    is_available = serializers.SerializerMethodField()
    stock_available = serializers.SerializerMethodField()
    
    class Meta:
        model = CartItem
        fields = [
            'id', 'product', 'product_name', 'product_price', 'product_sku',
            'product_details', 'quantity', 'total_price', 'is_available',
            'stock_available', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'product_name', 'product_price', 'product_sku', 
            'product_details', 'total_price', 'is_available', 
            'stock_available', 'created_at', 'updated_at'
        ]

    def get_total_price(self, obj):
        """
        Calculate total price for this cart item
        """
        return obj.quantity * obj.product.price

    def get_is_available(self, obj):
        """
        Check if product is still available
        """
        return obj.product.is_active and obj.product.stock_quantity > 0

    def get_stock_available(self, obj):
        """
        Get available stock for this product
        """
        return obj.product.stock_quantity

    def validate_quantity(self, value):
        """
        Validate quantity is positive
        """
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value

    def validate_product(self, value):
        """
        Validate product is active
        """
        if not value.is_active:
            raise serializers.ValidationError("This product is not available.")
        return value

    def validate(self, attrs):
        """
        Validate stock availability
        """
        product = attrs.get('product', self.instance.product if self.instance else None)
        quantity = attrs.get('quantity', self.instance.quantity if self.instance else 0)
        
        if product and quantity > product.stock_quantity:
            raise serializers.ValidationError({
                'quantity': f'Only {product.stock_quantity} items available in stock.'
            })
        
        return attrs


class CartSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for shopping carts
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    cart_items = CartItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    has_unavailable_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'user', 'user_name', 'cart_items', 'total_items',
            'total_amount', 'has_unavailable_items', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'user_name', 'cart_items', 'total_items',
            'total_amount', 'has_unavailable_items', 'created_at', 'updated_at'
        ]

    def get_total_items(self, obj):
        """
        Get total number of items in cart
        """
        return sum(item.quantity for item in obj.cart_items.all())

    def get_total_amount(self, obj):
        """
        Calculate total cart amount
        """
        return sum(
            item.quantity * item.product.price 
            for item in obj.cart_items.all() 
            if item.product.is_active
        )

    def get_has_unavailable_items(self, obj):
        """
        Check if cart has any unavailable items
        """
        return any(
            not item.product.is_active or item.product.stock_quantity == 0
            for item in obj.cart_items.all()
        )


class AddToCartSerializer(serializers.Serializer):
    """
    Serializer for adding items to cart
    """
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1, default=1)

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
            
            # Check current cart quantity for this product
            user = self.context['request'].user
            cart = Cart.objects.get_or_create(user=user)[0]
            
            existing_item = cart.cart_items.filter(product=product).first()
            current_quantity = existing_item.quantity if existing_item else 0
            total_quantity = current_quantity + quantity
            
            if total_quantity > product.stock_quantity:
                available = product.stock_quantity - current_quantity
                if available <= 0:
                    raise serializers.ValidationError({
                        'quantity': 'This product is out of stock.'
                    })
                else:
                    raise serializers.ValidationError({
                        'quantity': f'Only {available} more items can be added to cart.'
                    })
        except Product.DoesNotExist:
            pass  # Will be caught by product_id validation
        
        return attrs

    @transaction.atomic
    def save(self):
        """
        Add item to user's cart
        """
        user = self.context['request'].user
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        
        # Get or create cart
        cart, created = Cart.objects.get_or_create(user=user)
        
        # Get product
        product = Product.objects.get(id=product_id)
        
        # Get or create cart item
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not item_created:
            # Update quantity if item already exists
            cart_item.quantity += quantity
            cart_item.save()
        
        return cart_item


class UpdateCartItemSerializer(serializers.Serializer):
    """
    Serializer for updating cart item quantity
    """
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        """
        Validate stock availability
        """
        quantity = attrs['quantity']
        cart_item = self.instance
        
        if quantity > cart_item.product.stock_quantity:
            raise serializers.ValidationError({
                'quantity': f'Only {cart_item.product.stock_quantity} items available in stock.'
            })
        
        return attrs

    def save(self):
        """
        Update cart item quantity
        """
        self.instance.quantity = self.validated_data['quantity']
        self.instance.save()
        return self.instance


class CartSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight cart summary for checkout
    """
    total_items = serializers.SerializerMethodField()
    total_amount = serializers.SerializerMethodField()
    available_items = serializers.SerializerMethodField()
    unavailable_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = [
            'id', 'total_items', 'total_amount', 
            'available_items', 'unavailable_items'
        ]

    def get_total_items(self, obj):
        """
        Get total number of items in cart
        """
        return sum(item.quantity for item in obj.cart_items.all())

    def get_total_amount(self, obj):
        """
        Calculate total cart amount for available items only
        """
        return sum(
            item.quantity * item.product.price 
            for item in obj.cart_items.all() 
            if item.product.is_active and item.product.stock_quantity >= item.quantity
        )

    def get_available_items(self, obj):
        """
        Get count of available items
        """
        return sum(
            item.quantity for item in obj.cart_items.all()
            if item.product.is_active and item.product.stock_quantity >= item.quantity
        )

    def get_unavailable_items(self, obj):
        """
        Get count of unavailable items
        """
        return sum(
            item.quantity for item in obj.cart_items.all()
            if not item.product.is_active or item.product.stock_quantity < item.quantity
        )


class ClearCartSerializer(serializers.Serializer):
    """
    Serializer for clearing cart
    """
    confirm = serializers.BooleanField(default=False)

    def validate_confirm(self, value):
        """
        Validate confirmation
        """
        if not value:
            raise serializers.ValidationError("Confirmation required to clear cart.")
        return value

    def save(self):
        """
        Clear all items from cart
        """
        user = self.context['request'].user
        try:
            cart = Cart.objects.get(user=user)
            cart.cart_items.all().delete()
            return cart
        except Cart.DoesNotExist:
            # Cart doesn't exist, nothing to clear
            return None
