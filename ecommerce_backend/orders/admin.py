from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items"""
    model = OrderItem
    extra = 0
    fields = ('product', 'quantity', 'unit_price', 'total_price')
    readonly_fields = ('total_price',)
    ordering = ('created_at',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Comprehensive order administration"""
    list_display = ('order_number', 'user_email', 'status_colored', 'total_amount', 'item_count_display', 'payment_method', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'user__email', 'user__first_name', 'user__last_name')
    readonly_fields = ('order_number', 'created_at', 'updated_at', 'shipping_address_display', 'billing_address_display')
    inlines = [OrderItemInline]
    
    fieldsets = (
        ('Order Information', {
            'fields': ('order_number', 'user', 'status', 'total_amount')
        }),
        ('Payment & Shipping', {
            'fields': ('payment_method', 'shipping_address_display', 'billing_address_display')
        }),
        ('Additional Information', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def user_email(self, obj):
        """Display user email with link to user admin"""
        url = reverse('admin:authentication_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.email)
    user_email.short_description = 'Customer'
    user_email.admin_order_field = 'user__email'
    
    def status_colored(self, obj):
        """Display status with color coding"""
        colors = {
            'pending': 'orange',
            'confirmed': 'blue',
            'processing': 'purple',
            'shipped': 'green',
            'delivered': 'darkgreen',
            'cancelled': 'red',
        }
        color = colors.get(obj.status, 'black')
        return format_html('<span style="color: {}; font-weight: bold;">{}</span>', 
                         color, obj.get_status_display())
    status_colored.short_description = 'Status'
    status_colored.admin_order_field = 'status'
    
    def item_count_display(self, obj):
        """Display number of items in order"""
        count = obj.item_count
        return f"{count} item{'s' if count != 1 else ''}"
    item_count_display.short_description = 'Items'
    
    def shipping_address_display(self, obj):
        """Format shipping address for display"""
        if obj.shipping_address:
            addr = obj.shipping_address
            return format_html(
                '<div>{}<br/>{}, {}</div>',
                addr.get('street', ''),
                addr.get('city', ''),
                addr.get('country', '')
            )
        return "No address"
    shipping_address_display.short_description = 'Shipping Address'
    
    def billing_address_display(self, obj):
        """Format billing address for display"""
        if obj.billing_address:
            addr = obj.billing_address
            return format_html(
                '<div>{}<br/>{}, {}</div>',
                addr.get('street', ''),
                addr.get('city', ''),
                addr.get('country', '')
            )
        return "Same as shipping"
    billing_address_display.short_description = 'Billing Address'
    
    actions = ['mark_confirmed', 'mark_processing', 'mark_shipped']
    
    def mark_confirmed(self, request, queryset):
        """Bulk confirm orders"""
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed.')
    mark_confirmed.short_description = 'Mark selected orders as confirmed'
    
    def mark_processing(self, request, queryset):
        """Bulk mark orders as processing"""
        updated = queryset.update(status='processing')
        self.message_user(request, f'{updated} orders marked as processing.')
    mark_processing.short_description = 'Mark selected orders as processing'
    
    def mark_shipped(self, request, queryset):
        """Bulk mark orders as shipped"""
        updated = queryset.update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_shipped.short_description = 'Mark selected orders as shipped'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Order item administration"""
    list_display = ('order_number', 'product_name', 'quantity', 'unit_price', 'total_price', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('order__order_number', 'product__name', 'product__sku')
    readonly_fields = ('total_price', 'created_at')
    ordering = ('-created_at',)
    
    def order_number(self, obj):
        """Display order number with link"""
        url = reverse('admin:orders_order_change', args=[obj.order.pk])
        return format_html('<a href="{}">{}</a>', url, obj.order.order_number)
    order_number.short_description = 'Order'
    order_number.admin_order_field = 'order__order_number'
    
    def product_name(self, obj):
        """Display product name with link"""
        url = reverse('admin:products_product_change', args=[obj.product.pk])
        return format_html('<a href="{}">{}</a>', url, obj.product.name)
    product_name.short_description = 'Product'
    product_name.admin_order_field = 'product__name'
