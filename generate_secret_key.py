#!/usr/bin/env python3
"""
Generate Django Secret Key for Production
Run: python generate_secret_key.py
"""

import os
import sys

# Add Django to path
sys.path.append('ecommerce_backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

try:
    from django.core.management.utils import get_random_secret_key
    
    secret_key = get_random_secret_key()
    print("=" * 60)
    print("DJANGO SECRET KEY FOR PRODUCTION")
    print("=" * 60)
    print(f"SECRET_KEY={secret_key}")
    print("=" * 60)
    print("Copy the line above to your Render environment variables")
    print("=" * 60)
    
except ImportError:
    print("Django not found. Please run from the project root directory.")
    print("Or generate manually with:")
    print("python -c \"from django.core.management.utils import get_random_secret_key; print('SECRET_KEY=' + get_random_secret_key())\"")
