#!/usr/bin/env bash
# Build script for Render deployment

set -o errexit  # exit on error

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=config.settings.production

# Install Python dependencies
pip install --upgrade pip
pip install -r ecommerce_backend/requirements.txt

# Change to backend directory for Django commands
cd ecommerce_backend

# Collect static files 
python django_manage.py collectstatic --noinput

# Run migrations in the correct order to handle custom User model
python django_manage.py migrate auth --noinput
python django_manage.py migrate contenttypes --noinput  
python django_manage.py migrate authentication --noinput
python django_manage.py migrate --run-syncdb --noinput

# Create demo superuser for admin access
python django_manage.py create_demo_superuser
