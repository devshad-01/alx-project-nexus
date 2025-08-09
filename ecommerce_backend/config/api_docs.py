"""
API Documentation views for ALX Project Nexus

This module provides API documentation and schema endpoints.
"""

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([AllowAny])
def api_documentation_view(request):
    """
    API Documentation endpoint.
    
    Returns comprehensive API documentation with all available endpoints.
    """
    documentation = {
        "api_info": {
            "name": "ALX Project Nexus E-commerce API",
            "version": "1.0.0",
            "description": "RESTful API for e-commerce backend with authentication, products, orders, and cart functionality",
            "base_url": request.build_absolute_uri('/api/'),
        },
        "authentication": {
            "type": "JWT Bearer Token",
            "description": "Use JWT tokens for authentication. Include in headers as: Authorization: Bearer <token>",
            "endpoints": {
                "POST /api/auth/register/": "User registration",
                "POST /api/auth/login/": "User login (get tokens)",
                "POST /api/auth/logout/": "User logout (blacklist token)",
                "POST /api/auth/refresh/": "Refresh access token",
                "GET /api/auth/profile/": "Get user profile",
                "PATCH /api/auth/profile/update/": "Update user profile",
                "PATCH /api/auth/change-password/": "Change password",
                "GET /api/auth/status/": "Check authentication status",
                "GET /api/auth/users/": "List all users (admin only)"
            }
        },
        "products": {
            "description": "Product and category management",
            "endpoints": {
                "GET /api/products/": "List products with filtering and pagination",
                "POST /api/products/": "Create product (admin only)",
                "GET /api/products/<slug>/": "Get product details",
                "PATCH /api/products/<slug>/": "Update product (admin only)",
                "DELETE /api/products/<slug>/": "Delete product (admin only)",
                "GET /api/products/categories/": "List categories",
                "POST /api/products/categories/": "Create category (admin only)",
                "GET /api/products/categories/<slug>/": "Get category details",
                "GET /api/products/<slug>/reviews/": "List product reviews",
                "POST /api/products/<slug>/reviews/": "Create product review",
                "GET /api/products/search/": "Search products",
                "GET /api/products/featured/": "Get featured products"
            },
            "filters": {
                "category": "Filter by category ID",
                "is_available": "Filter by availability (true/false)",
                "min_price": "Minimum price filter",
                "max_price": "Maximum price filter",
                "min_rating": "Minimum rating filter",
                "search": "Search in name, description, category"
            }
        },
        "orders": {
            "description": "Order management and tracking",
            "endpoints": {
                "GET /api/orders/": "List user's orders",
                "POST /api/orders/": "Create new order",
                "GET /api/orders/<order_number>/": "Get order details",
                "PATCH /api/orders/<order_number>/": "Update order (limited fields)",
                "DELETE /api/orders/<order_number>/": "Cancel order",
                "GET /api/orders/<order_number>/track/": "Track order status",
                "GET /api/orders/statistics/": "Get order statistics",
                "GET /api/orders/admin/all/": "List all orders (admin only)",
                "PATCH /api/orders/admin/<order_number>/status/": "Update order status (admin only)"
            },
            "order_statuses": ["pending", "processing", "shipped", "delivered", "cancelled"]
        },
        "cart": {
            "description": "Shopping cart functionality",
            "endpoints": {
                "GET /api/cart/": "Get user's cart",
                "POST /api/cart/add/": "Add item to cart",
                "PATCH /api/cart/update/<item_id>/": "Update cart item quantity",
                "DELETE /api/cart/remove/<item_id>/": "Remove item from cart",
                "DELETE /api/cart/clear/": "Clear entire cart",
                "GET /api/cart/summary/": "Get cart summary",
                "POST /api/checkout/validate/": "Validate cart before checkout"
            }
        },
        "utilities": {
            "description": "General utility endpoints",
            "endpoints": {
                "GET /api/health/": "API health check",
                "GET /api/info/": "API information",
                "GET /api/docs/": "This documentation"
            }
        },
        "response_format": {
            "success": {
                "description": "Successful responses include relevant data",
                "example": {
                    "message": "Operation successful",
                    "data": "{ ... response data ... }"
                }
            },
            "error": {
                "description": "Error responses include error details",
                "example": {
                    "error": "Error message",
                    "details": "{ ... error details ... }"
                }
            }
        },
        "pagination": {
            "description": "List endpoints support pagination",
            "parameters": {
                "page": "Page number (default: 1)",
                "page_size": "Items per page (default: 20, max: 100)"
            },
            "response_format": {
                "count": "Total number of items",
                "next": "URL to next page",
                "previous": "URL to previous page",
                "results": "Array of items"
            }
        }
    }
    
    return Response(documentation, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def api_endpoints_view(request):
    """
    Quick reference of all API endpoints.
    
    Returns a simple list of all available endpoints.
    """
    base_url = request.build_absolute_uri('/api/')
    
    endpoints = {
        "Authentication": [
            f"{base_url}auth/register/",
            f"{base_url}auth/login/",
            f"{base_url}auth/logout/",
            f"{base_url}auth/refresh/",
            f"{base_url}auth/profile/",
            f"{base_url}auth/profile/update/",
            f"{base_url}auth/change-password/",
            f"{base_url}auth/status/",
            f"{base_url}auth/users/"
        ],
        "Products": [
            f"{base_url}products/",
            f"{base_url}products/<slug>/",
            f"{base_url}products/categories/",
            f"{base_url}products/categories/<slug>/",
            f"{base_url}products/<slug>/reviews/",
            f"{base_url}products/search/",
            f"{base_url}products/featured/"
        ],
        "Orders": [
            f"{base_url}orders/",
            f"{base_url}orders/<order_number>/",
            f"{base_url}orders/<order_number>/track/",
            f"{base_url}orders/statistics/",
            f"{base_url}orders/admin/all/",
            f"{base_url}orders/admin/<order_number>/status/"
        ],
        "Cart": [
            f"{base_url}cart/",
            f"{base_url}cart/add/",
            f"{base_url}cart/update/<item_id>/",
            f"{base_url}cart/remove/<item_id>/",
            f"{base_url}cart/clear/",
            f"{base_url}cart/summary/",
            f"{base_url}checkout/validate/"
        ],
        "Utilities": [
            f"{base_url}health/",
            f"{base_url}info/",
            f"{base_url}docs/",
            f"{base_url}endpoints/"
        ]
    }
    
    return Response(endpoints, status=status.HTTP_200_OK)
