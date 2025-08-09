from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Category, Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images"""
    model = ProductImage
    extra = 1
    fields = ('image_url', 'alt_text', 'is_primary', 'sort_order')
    ordering = ('sort_order', 'created_at')


class ReviewInline(admin.TabularInline):
    """Inline admin for product reviews"""
    model = Review
    extra = 0
    fields = ('user', 'rating', 'title', 'is_approved', 'helpful_count')
    readonly_fields = ('helpful_count',)
    ordering = ('-created_at',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Enhanced category administration"""
    list_display = ('name', 'slug', 'product_count', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('name',)
    
    def product_count(self, obj):
        """Display number of products in category"""
        count = obj.products.count()
        url = reverse('admin:products_product_changelist') + f'?category__id__exact={obj.id}'
        return format_html('<a href="{}">{} products</a>', url, count)
    product_count.short_description = 'Products'


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Comprehensive product administration"""
    list_display = ('name', 'category', 'price', 'stock_quantity', 'is_active', 'is_featured', 'review_summary', 'created_at')
    list_filter = ('category', 'is_active', 'is_featured', 'created_at', 'created_by')
    search_fields = ('name', 'sku', 'description')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at', 'review_summary_detailed', 'stock_status')
    filter_horizontal = ()
    inlines = [ProductImageInline, ReviewInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'description', 'category')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'sku', 'stock_quantity', 'stock_status')
        }),
        ('Status & Features', {
            'fields': ('is_active', 'is_featured', 'created_by')
        }),
        ('Reviews & Ratings', {
            'fields': ('review_summary_detailed',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def stock_status(self, obj):
        """Display stock status with color coding"""
        if obj.stock_quantity > 20:
            color = 'green'
            status = 'In Stock'
        elif obj.stock_quantity > 0:
            color = 'orange'
            status = 'Low Stock'
        else:
            color = 'red'
            status = 'Out of Stock'
        return format_html('<span style="color: {};">{}</span>', color, status)
    stock_status.short_description = 'Stock Status'
    
    def review_summary(self, obj):
        """Display review summary in list view"""
        avg_rating = obj.average_rating
        review_count = obj.review_count
        if review_count > 0:
            stars = '★' * int(avg_rating) + '☆' * (5 - int(avg_rating))
            return f"{stars} ({review_count})"
        return "No reviews"
    review_summary.short_description = 'Reviews'
    
    def review_summary_detailed(self, obj):
        """Detailed review summary for detail view"""
        avg_rating = obj.average_rating
        review_count = obj.review_count
        if review_count > 0:
            return f"Average Rating: {avg_rating:.1f}/5.0 ({review_count} reviews)"
        return "No reviews yet"
    review_summary_detailed.short_description = 'Review Summary'
    
    def save_model(self, request, obj, form, change):
        """Auto-assign created_by field"""
        if not change:  # Only for new objects
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    """Product image administration"""
    list_display = ('product', 'image_preview', 'alt_text', 'is_primary', 'sort_order', 'created_at')
    list_filter = ('is_primary', 'created_at')
    search_fields = ('product__name', 'alt_text')
    ordering = ('product', 'sort_order', 'created_at')
    
    def image_preview(self, obj):
        """Display image preview in admin"""
        if obj.image_url:
            return format_html('<img src="{}" style="max-height: 50px; max-width: 100px;" />', obj.image_url)
        return "No image"
    image_preview.short_description = 'Preview'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """Product review administration"""
    list_display = ('product', 'user', 'rating', 'title', 'is_approved', 'is_verified', 'helpful_count', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_verified', 'created_at')
    search_fields = ('product__name', 'user__email', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Review Information', {
            'fields': ('user', 'product', 'rating', 'title', 'comment')
        }),
        ('Moderation', {
            'fields': ('is_approved', 'is_verified', 'helpful_count')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        """Bulk approve reviews"""
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} reviews approved.')
    approve_reviews.short_description = 'Approve selected reviews'
    
    def disapprove_reviews(self, request, queryset):
        """Bulk disapprove reviews"""
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} reviews disapproved.')
    disapprove_reviews.short_description = 'Disapprove selected reviews'
