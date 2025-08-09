from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings


class Cart(models.Model):
    """User shopping cart management"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        indexes = [
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"Cart for {self.user.email}"

    @property
    def total_items(self):
        """Get total number of items in cart"""
        return self.items.aggregate(
            total=models.Sum('quantity')
        )['total'] or 0

    @property
    def total_price(self):
        """Calculate total price of all items in cart"""
        total = 0
        for item in self.items.all():
            total += item.total_price
        return total


class CartItem(models.Model):
    """Individual items within shopping carts"""
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='cart_items'
    )
    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    added_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cart_items'
        unique_together = ['cart', 'product']
        indexes = [
            models.Index(fields=['cart']),
            models.Index(fields=['product']),
            models.Index(fields=['cart', 'product']),
        ]

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.cart.user.email}'s cart"

    @property
    def total_price(self):
        """Calculate total price for this cart item"""
        return self.product.price * self.quantity
