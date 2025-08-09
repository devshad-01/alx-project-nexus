"""
Core URL Configuration for ALX Project Nexus

This module defines URL patterns for cart and utility endpoints.
"""

from django.urls import path

from . import views

app_name = 'core'

urlpatterns = [
    # Cart endpoints
    path('cart/', views.CartView.as_view(), name='cart'),
    path('cart/add/', views.add_to_cart_view, name='add_to_cart'),
    path('cart/update/<int:item_id>/', views.update_cart_item_view, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name='remove_from_cart'),
    path('cart/clear/', views.clear_cart_view, name='clear_cart'),
    path('cart/summary/', views.cart_summary_view, name='cart_summary'),
    
    # Checkout utilities
    path('checkout/validate/', views.checkout_validation_view, name='checkout_validation'),
    
    # Utility endpoints
    path('health/', views.health_check_view, name='health_check'),
    path('info/', views.api_info_view, name='api_info'),
]
