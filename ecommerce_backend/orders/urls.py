"""
Orders URL Configuration for ALX Project Nexus

This module defines URL patterns for order management endpoints.
"""

from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    # Order endpoints
    path('', views.OrderListView.as_view(), name='order_list'),
    path('<str:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),
    
    # Order tracking
    path('<str:order_number>/track/', views.track_order_view, name='track_order'),
    
    # Order statistics
    path('statistics/', views.order_statistics_view, name='order_statistics'),
    
    # Admin endpoints
    path('admin/all/', views.AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/<str:order_number>/status/', views.update_order_status_view, name='update_order_status'),
]
