#!/bin/bash

# ALX Project Nexus - Development Environment Activation Script
# This script helps you easily work with the virtual environment

PROJECT_ROOT="/home/shad/Desktop/alx_project_nexus"
BACKEND_DIR="$PROJECT_ROOT/ecommerce_backend"
VENV_DIR="$BACKEND_DIR/venv"

echo "🚀 ALX Project Nexus - Development Environment"
echo "================================================"

# Check if we're in the right directory
if [ ! -d "$BACKEND_DIR" ]; then
    echo "❌ Error: Backend directory not found at $BACKEND_DIR"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Error: Virtual environment not found at $VENV_DIR"
    echo "Please create it first with: python3 -m venv $VENV_DIR"
    exit 1
fi

# Change to backend directory
cd "$BACKEND_DIR"
echo "📁 Changed to backend directory: $(pwd)"

# Activate virtual environment
source "$VENV_DIR/bin/activate"
echo "✅ Virtual environment activated"

# Show Python and pip versions
echo "🐍 Python version: $(python --version)"
echo "📦 Pip version: $(pip --version)"

# Check if Django is installed
if python -c "import django" 2>/dev/null; then
    echo "✅ Django is installed: $(python -c "import django; print(django.get_version())")"
else
    echo "⚠️  Django is not installed. Installing dependencies..."
    pip install -r requirements.txt
fi

echo "================================================"
echo "🎯 Environment is ready!"
echo ""
echo "Common commands:"
echo "  python manage.py runserver     # Start development server"
echo "  python manage.py migrate       # Run database migrations"  
echo "  python manage.py shell         # Open Django shell"
echo "  python manage.py createsuperuser # Create admin user"
echo "  python manage.py check         # Check for issues"
echo ""
echo "To deactivate virtual environment, run: deactivate"
echo "================================================"

# Start a new shell with the environment activated
exec "$SHELL"
