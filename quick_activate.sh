#!/bin/bash

# Quick activation script for ALX Project Nexus
# Usage: source quick_activate.sh

echo "🔥 Quick activating ALX Project Nexus environment..."

# Navigate to backend directory and activate environment
cd /home/shad/Desktop/alx_project_nexus/ecommerce_backend
source venv/bin/activate

echo "✅ Environment activated! You're now in $(pwd)"
echo "🐍 Using Python: $(which python)"
echo ""
echo "Ready to use commands like:"
echo "  python manage.py runserver"
echo "  python manage.py check"
echo "  python manage.py migrate"
