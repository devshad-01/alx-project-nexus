"""
Products serializers for ALX Project Nexus E-Commerce Backend
Handles product catalogs, categories, images, and reviews
"""

from rest_framework import serializers
from decimal import Decimal
from django.db.models import Avg, Count
from .models import Category, Product, ProductImage, Review


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for product categories
    """
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 
            'is_active', 'product_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'product_count']

    def get_product_count(self, obj):
        """
        Get count of active products in this category
        """
        return obj.products.filter(is_active=True).count()

    def validate_name(self, value):
        """
        Validate category name uniqueness
        """
        if self.instance:
            # Update case - exclude current instance
            if Category.objects.filter(name=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A category with this name already exists.")
        else:
            # Create case
            if Category.objects.filter(name=value).exists():
                raise serializers.ValidationError("A category with this name already exists.")
        return value


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Serializer for product images
    """
    
    class Meta:
        model = ProductImage
        fields = [
            'id', 'image_url', 'alt_text', 'is_primary', 
            'sort_order', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, attrs):
        """
        Validate image constraints
        """
        # Ensure only one primary image per product
        if attrs.get('is_primary', False):
            product = attrs.get('product') or (self.instance.product if self.instance else None)
            if product:
                existing_primary = ProductImage.objects.filter(
                    product=product, is_primary=True
                )
                if self.instance:
                    existing_primary = existing_primary.exclude(pk=self.instance.pk)
                
                if existing_primary.exists():
                    raise serializers.ValidationError({
                        'is_primary': 'A product can only have one primary image.'
                    })
        
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for product reviews
    """
    user_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_name', 'user_username', 'product', 
            'rating', 'title', 'comment', 'is_approved', 'is_verified',
            'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'user', 'user_name', 'user_username', 
            'is_approved', 'is_verified', 'created_at', 'updated_at'
        ]

    def validate_rating(self, value):
        """
        Validate rating is within range
        """
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, attrs):
        """
        Validate user hasn't already reviewed this product
        """
        user = self.context['request'].user
        product = attrs['product']
        
        if self.instance:
            # Update case - exclude current review
            existing_review = Review.objects.filter(
                user=user, product=product
            ).exclude(pk=self.instance.pk)
        else:
            # Create case
            existing_review = Review.objects.filter(user=user, product=product)
        
        if existing_review.exists():
            raise serializers.ValidationError({
                'product': 'You have already reviewed this product.'
            })
        
        return attrs


class ProductSerializer(serializers.ModelSerializer):
    """
    Comprehensive serializer for products with all related data
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    
    # Calculated fields
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    discounted_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'discounted_price',
            'category', 'category_name', 'sku', 'stock_quantity',
            'is_in_stock', 'is_active', 'is_featured', 'slug',
            'images', 'primary_image', 'reviews', 'average_rating',
            'review_count', 'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = [
            'id', 'category_name', 'images', 'reviews', 'average_rating',
            'review_count', 'primary_image', 'is_in_stock', 'discounted_price',
            'created_by', 'created_at', 'updated_at'
        ]

    def get_average_rating(self, obj):
        """
        Calculate average rating from approved reviews
        """
        avg = obj.reviews.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        return round(float(avg), 2) if avg else 0.0

    def get_review_count(self, obj):
        """
        Get count of approved reviews
        """
        return obj.reviews.filter(is_approved=True).count()

    def get_primary_image(self, obj):
        """
        Get primary image URL or first image
        """
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return {
                'id': primary_image.id,
                'image_url': primary_image.image_url,
                'alt_text': primary_image.alt_text
            }
        
        # Return first image if no primary image
        first_image = obj.images.first()
        if first_image:
            return {
                'id': first_image.id,
                'image_url': first_image.image_url,
                'alt_text': first_image.alt_text
            }
        
        return None

    def get_is_in_stock(self, obj):
        """
        Check if product is in stock
        """
        return obj.stock_quantity > 0

    def get_discounted_price(self, obj):
        """
        Calculate discounted price if applicable
        """
        # You can implement discount logic here
        # For now, return the original price
        return obj.price

    def validate_sku(self, value):
        """
        Validate SKU uniqueness
        """
        if self.instance:
            # Update case - exclude current instance
            if Product.objects.filter(sku=value).exclude(pk=self.instance.pk).exists():
                raise serializers.ValidationError("A product with this SKU already exists.")
        else:
            # Create case
            if Product.objects.filter(sku=value).exists():
                raise serializers.ValidationError("A product with this SKU already exists.")
        return value

    def validate_price(self, value):
        """
        Validate price is positive
        """
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    def validate_stock_quantity(self, value):
        """
        Validate stock quantity is non-negative
        """
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value


class ProductListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for product lists and search results
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    primary_image = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    is_in_stock = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'price', 'category', 'category_name',
            'sku', 'is_in_stock', 'is_featured', 'primary_image',
            'average_rating', 'review_count', 'created_at'
        ]

    def get_primary_image(self, obj):
        """
        Get primary image URL only
        """
        primary_image = obj.images.filter(is_primary=True).first()
        if primary_image:
            return primary_image.image_url
        
        first_image = obj.images.first()
        return first_image.image_url if first_image else None

    def get_average_rating(self, obj):
        """
        Use annotated average rating from queryset if available
        """
        if hasattr(obj, 'annotated_avg_rating') and obj.annotated_avg_rating is not None:
            return round(float(obj.annotated_avg_rating), 2)
        
        # Fallback to manual calculation
        avg = obj.reviews.filter(is_approved=True).aggregate(
            avg_rating=Avg('rating')
        )['avg_rating']
        return round(float(avg), 2) if avg else 0.0

    def get_review_count(self, obj):
        """
        Use annotated review count from queryset if available
        """
        if hasattr(obj, 'annotated_review_count'):
            return obj.annotated_review_count
            
        # Fallback to manual count
        return obj.reviews.filter(is_approved=True).count()

    def get_is_in_stock(self, obj):
        """
        Check stock status
        """
        return obj.stock_quantity > 0


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Serializer for creating new products
    """
    images = ProductImageSerializer(many=True, required=False)
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'category', 'sku',
            'stock_quantity', 'is_active', 'is_featured', 'images'
        ]

    def create(self, validated_data):
        """
        Create product with images
        """
        images_data = validated_data.pop('images', [])
        
        # Set created_by to current user
        validated_data['created_by'] = self.context['request'].user
        
        product = Product.objects.create(**validated_data)
        
        # Create images
        for image_data in images_data:
            ProductImage.objects.create(product=product, **image_data)
        
        return product

    def validate_sku(self, value):
        """
        Validate SKU uniqueness
        """
        if Product.objects.filter(sku=value).exists():
            raise serializers.ValidationError("A product with this SKU already exists.")
        return value


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Serializer for updating existing products
    """
    
    class Meta:
        model = Product
        fields = [
            'name', 'description', 'price', 'category',
            'stock_quantity', 'is_active', 'is_featured'
        ]

    def validate_sku(self, value):
        """
        Validate SKU uniqueness (excluding current product)
        """
        if Product.objects.filter(sku=value).exclude(pk=self.instance.pk).exists():
            raise serializers.ValidationError("A product with this SKU already exists.")
        return value


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Detailed category serializer with products
    """
    products = ProductListSerializer(many=True, read_only=True)
    product_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'slug', 'description', 'is_active',
            'product_count', 'products', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'slug', 'created_at', 'updated_at', 'product_count']

    def get_product_count(self, obj):
        """
        Get count of active products in this category
        """
        return obj.products.filter(is_active=True).count()
