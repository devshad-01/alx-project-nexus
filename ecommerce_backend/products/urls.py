"""
Products URL Configuration for ALX Project Nexus

This module defines URL patterns for product and category endpoints.
"""

from django.urls import path

from . import views

app_name = 'products'

urlpatterns = [
    # Category endpoints
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Product endpoints
    path('', views.ProductListView.as_view(), name='product_list'),
    path('<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    
    # Product reviews
    path('<slug:product_slug>/reviews/', views.ProductReviewListView.as_view(), name='product_reviews'),
    
    # Search and featured products
    path('search/', views.product_search_view, name='product_search'),
    path('featured/', views.featured_products_view, name='featured_products'),
]
