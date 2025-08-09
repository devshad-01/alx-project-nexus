#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

# Change to backend directory
cd ecommerce_backend

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Set Django settings for production
export DJANGO_SETTINGS_MODULE=config.settings.production

# Collect static files
python manage.py collectstatic --no-input

# Run database migrations
python manage.py migrate
