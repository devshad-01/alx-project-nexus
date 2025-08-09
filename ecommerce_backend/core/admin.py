from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    """Inline admin for cart items"""
    model = CartItem
    extra = 0
    fields = ('product', 'quantity', 'price_display', 'total_price_display')
    readonly_fields = ('price_display', 'total_price_display')
    ordering = ('-added_at',)
    
    def price_display(self, obj):
        """Display unit price"""
        return f"${obj.product.price:.2f}"
    price_display.short_description = 'Unit Price'
    
    def total_price_display(self, obj):
        """Display total price for cart item"""
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = 'Total Price'


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    """Shopping cart administration"""
    list_display = ('user_email', 'total_items_display', 'total_price_display', 'last_updated', 'created_at')
    search_fields = ('user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('created_at', 'updated_at', 'cart_summary')
    inlines = [CartItemInline]
    ordering = ('-updated_at',)
    
    fieldsets = (
        ('Cart Information', {
            'fields': ('user', 'cart_summary')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        """Display user email with link"""
        url = reverse('admin:authentication_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_email.short_description = 'Customer'
    user_email.admin_order_field = 'user__email'
    
    def total_items_display(self, obj):
        """Display total number of items"""
        count = obj.total_items
        return f"{count} item{'s' if count != 1 else ''}"
    total_items_display.short_description = 'Total Items'
    
    def total_price_display(self, obj):
        """Display total cart value"""
        total = obj.total_price
        if total > 0:
            return f"${total:.2f}"
        return "$0.00"
    total_price_display.short_description = 'Total Value'
    
    def last_updated(self, obj):
        """Display last update time"""
        return obj.updated_at.strftime("%Y-%m-%d %H:%M")
    last_updated.short_description = 'Last Updated'
    last_updated.admin_order_field = 'updated_at'
    
    def cart_summary(self, obj):
        """Display cart summary"""
        items = obj.total_items
        total = obj.total_price
        return f"{items} items worth ${total:.2f}"
    cart_summary.short_description = 'Cart Summary'
    
    actions = ['clear_empty_carts']
    
    def clear_empty_carts(self, request, queryset):
        """Remove carts with no items"""
        empty_carts = queryset.filter(items__isnull=True)
        count = empty_carts.count()
        empty_carts.delete()
        self.message_user(request, f'{count} empty carts removed.')
    clear_empty_carts.short_description = 'Clear empty carts'


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Cart item administration"""
    list_display = ('cart_user', 'product_name', 'quantity', 'unit_price', 'total_price_display', 'added_at')
    list_filter = ('added_at', 'updated_at')
    search_fields = ('cart__user__email', 'product__name', 'product__sku')
    readonly_fields = ('total_price_display', 'added_at', 'updated_at')
    ordering = ('-added_at',)
    
    def cart_user(self, obj):
        """Display cart owner"""
        url = reverse('admin:authentication_user_change', args=[obj.cart.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.cart.user.email)
    cart_user.short_description = 'Customer'
    cart_user.admin_order_field = 'cart__user__email'
    
    def product_name(self, obj):
        """Display product name with link"""
        url = reverse('admin:products_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_name.short_description = 'Product'
    product_name.admin_order_field = 'product__name'
    
    def unit_price(self, obj):
        """Display unit price"""
        return f"${obj.product.price:.2f}"
    unit_price.short_description = 'Unit Price'
    
    def total_price_display(self, obj):
        """Display total price for cart item"""
        return f"${obj.total_price:.2f}"
    total_price_display.short_description = 'Total Price'
