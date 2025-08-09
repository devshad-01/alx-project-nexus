#!/usr/bin/env bash
# Startup script for Render deployment

# Change to the Django project directory
cd ecommerce_backend

# Set Django settings for production
export DJANGO_SETTINGS_MODULE=config.settings.production

# Start gunicorn with proper configuration
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT --workers 1 --timeout 120
