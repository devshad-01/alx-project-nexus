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

#!/usr/bin/env bash
# Build script for Render deployment

# Set Django settings module for production
export DJANGO_SETTINGS_MODULE=config.settings.production

# Install Python dependencies
pip install -r ecommerce_backend/requirements.txt

# Collect static files 
cd ecommerce_backend
python django_manage.py collectstatic --noinput

# Run migrations in the correct order to handle custom User model
python django_manage.py migrate auth --noinput
python django_manage.py migrate contenttypes --noinput  
python django_manage.py migrate authentication --noinput
python django_manage.py migrate --run-syncdb --noinput
