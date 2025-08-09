"""
Main URL Configuration for ALX Project Nexus E-commerce Backend

This module defines the main URL patterns for the entire application.
Includes API endpoints for all apps and admin interface.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from .api_docs import api_documentation_view, api_endpoints_view

# API URL patterns
api_patterns = [
    path('auth/', include('authentication.urls')),
    path('products/', include('products.urls')),
    path('orders/', include('orders.urls')),
    path('', include('core.urls')),  # Cart and utility endpoints under /api/
    
    # API Documentation - drf-spectacular
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # Legacy API Documentation
    path('docs-legacy/', api_documentation_view, name='api_docs_legacy'),
    path('endpoints/', api_endpoints_view, name='api_endpoints'),
]

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/', include(api_patterns)),
]

# Add Django Debug Toolbar URLs in development
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
    
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
