# Deployment Guide - E-Commerce Backend

## 🚀 Deployment Overview

This guide provides comprehensive instructions for deploying the E-Commerce Backend API to various platforms. The application is designed to be deployment-ready with minimal configuration changes.

## 📋 Pre-Deployment Checklist

### Code Preparation
- [ ] All tests passing locally
- [ ] Environment variables documented
- [ ] Static files configuration verified
- [ ] Database migrations created and tested
- [ ] Security settings configured for production
- [ ] Requirements.txt updated with exact versions

### Environment Setup
- [ ] Production database created
- [ ] Redis instance available
- [ ] Static files storage configured
- [ ] Environment variables set
- [ ] SSL certificate ready
- [ ] Domain name configured

## 🐳 Docker Deployment

### Dockerfile
```dockerfile
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /app/

# Create static files directory
RUN mkdir -p /app/staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations and start server
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]
```

### Docker Compose (Local Development)
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DEBUG=False
      - DATABASE_URL=postgresql://postgres:password@db:5432/ecommerce_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - db
      - redis
    volumes:
      - ./staticfiles:/app/staticfiles
      - ./media:/app/media

  db:
    image: postgres:14
    environment:
      - POSTGRES_DB=ecommerce_db
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data/

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

volumes:
  postgres_data:
```

### Build and Deploy with Docker
```bash
# Build the image
docker build -t ecommerce-backend .

# Run with docker-compose
docker-compose up -d

# Apply migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# Load sample data
docker-compose exec web python manage.py loaddata fixtures/sample_data.json
```

## ☁️ Heroku Deployment

### Prerequisites
- Heroku CLI installed
- Git repository initialized
- Heroku account created

### Heroku Configuration Files

#### Procfile
```
web: gunicorn config.wsgi:application
release: python manage.py migrate
```

#### runtime.txt
```
python-3.9.18
```

#### requirements.txt (Production additions)
```
# Production dependencies
gunicorn==21.2.0
whitenoise==6.5.0
dj-database-url==2.1.0
psycopg2-binary==2.9.7
```

### Deployment Steps
```bash
# Login to Heroku
heroku login

# Create Heroku app
heroku create your-ecommerce-backend

# Add PostgreSQL addon
heroku addons:create heroku-postgresql:mini

# Add Redis addon
heroku addons:create heroku-redis:mini

# Set environment variables
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=your-app-name.herokuapp.com

# Deploy to Heroku
git push heroku main

# Run migrations
heroku run python manage.py migrate

# Create superuser
heroku run python manage.py createsuperuser

# Load sample data
heroku run python manage.py loaddata fixtures/sample_data.json
```

## 🌐 Railway Deployment

### Railway Configuration

#### railway.toml
```toml
[build]
builder = "nixpacks"

[deploy]
healthcheckPath = "/api/health/"
restartPolicyType = "on_failure"
restartPolicyMaxRetries = 3

[[services]]
name = "web"
```

### Deployment Steps
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Initialize project
railway init

# Link to existing project or create new
railway link

# Set environment variables
railway variables set DEBUG=False
railway variables set SECRET_KEY=your-secret-key
railway variables set PYTHONPATH=/app

# Deploy
railway up

# Run migrations
railway run python manage.py migrate

# Create superuser
railway run python manage.py createsuperuser
```

## ⚡ DigitalOcean App Platform

### App Spec Configuration (app.yaml)
```yaml
name: ecommerce-backend
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo
    branch: main
  run_command: gunicorn --worker-tmp-dir /dev/shm config.wsgi:application
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  env:
  - key: DEBUG
    value: "False"
  - key: SECRET_KEY
    value: your-secret-key
    type: SECRET
  - key: DATABASE_URL
    value: ${db.DATABASE_URL}
  - key: REDIS_URL
    value: ${redis.REDIS_URL}

databases:
- name: db
  engine: PG
  size: basic-xxs

- name: redis
  engine: REDIS
  size: basic-xxs
```

## 🔧 Production Settings Configuration

### settings/production.py
```python
import os
import dj_database_url
from .base import *

# Security settings
DEBUG = False
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# Database configuration
DATABASES = {
    'default': dj_database_url.parse(os.getenv('DATABASE_URL'))
}

# Static files with WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (use cloud storage in production)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.getenv('AWS_S3_REGION_NAME', 'us-east-1')

# Redis configuration
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# SSL settings
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

## 🔐 Environment Variables

### Required Environment Variables
```bash
# Django settings
SECRET_KEY=your-super-secret-key-here
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Redis
REDIS_URL=redis://host:port/db

# AWS S3 (for media files)
AWS_ACCESS_KEY_ID=your-access-key
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Email settings (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# API Keys (if using external services)
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
```

### Environment File Template (.env.production)
```bash
# Copy this template and fill in your values
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=

DATABASE_URL=
REDIS_URL=

AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_STORAGE_BUCKET_NAME=
AWS_S3_REGION_NAME=

EMAIL_HOST=
EMAIL_PORT=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

## 🚨 Post-Deployment Verification

### Health Check Endpoint
Create a health check endpoint for monitoring:

```python
# views.py
from django.http import JsonResponse
from django.db import connection

def health_check(request):
    """Health check endpoint for monitoring"""
    try:
        # Check database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        
        return JsonResponse({
            'status': 'healthy',
            'database': 'connected',
            'timestamp': timezone.now().isoformat()
        })
    except Exception as e:
        return JsonResponse({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': timezone.now().isoformat()
        }, status=503)
```

### Verification Checklist
```bash
# Test API endpoints
curl https://your-domain.com/api/health/
curl https://your-domain.com/api/products/
curl https://your-domain.com/api/categories/

# Test authentication
curl -X POST https://your-domain.com/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass"}'

# Verify SSL certificate
curl -I https://your-domain.com/

# Check static files
curl https://your-domain.com/static/admin/css/base.css

# Test admin interface
# Visit: https://your-domain.com/admin/
```

## 📊 Monitoring and Maintenance

### Application Monitoring
- Set up error tracking (Sentry)
- Monitor response times (New Relic/DataDog)
- Database performance monitoring
- SSL certificate expiration alerts

### Regular Maintenance Tasks
```bash
# Weekly maintenance script
#!/bin/bash

# Update dependencies
pip install -r requirements.txt --upgrade

# Run database optimizations
python manage.py dbshell < maintenance/optimize_db.sql

# Clear expired sessions
python manage.py clearsessions

# Update search indexes (if using search)
python manage.py update_index

# Backup database
pg_dump $DATABASE_URL > backups/backup_$(date +%Y%m%d).sql
```

### Security Updates
- Regularly update Django and dependencies
- Monitor security advisories
- Review and rotate API keys
- Update SSL certificates
- Review user permissions

## 🛡️ Security Considerations

### Production Security Checklist
- [ ] DEBUG=False in production
- [ ] Strong SECRET_KEY generated
- [ ] Database credentials secured
- [ ] SSL/TLS enabled
- [ ] Security headers configured
- [ ] CORS properly configured
- [ ] Rate limiting enabled
- [ ] Input validation implemented
- [ ] SQL injection prevention verified
- [ ] XSS protection enabled

### Backup Strategy
- Daily automated database backups
- Media files backup to cloud storage
- Configuration backup
- Regular backup restoration testing

---

**Note**: This deployment guide covers the most common deployment scenarios. Adapt the configurations based on your specific requirements and platform constraints.

**Support**: For deployment issues, refer to the platform-specific documentation or consult the deployment troubleshooting section in the project wiki.
