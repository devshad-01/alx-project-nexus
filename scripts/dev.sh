#!/bin/bash

# Quick Development Environment Setup
# Usage: ./dev.sh [command]
# If no command provided, opens interactive shell

PROJECT_ROOT="/home/shad/Desktop/alx_project_nexus"
BACKEND_DIR="$PROJECT_ROOT/ecommerce_backend"
VENV_DIR="$BACKEND_DIR/venv"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "❌ Error: Virtual environment not found at $VENV_DIR"
    exit 1
fi

# Change to backend directory
cd "$BACKEND_DIR"

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# If command provided, run it; otherwise start interactive shell
if [ $# -eq 0 ]; then
    echo "🚀 Development environment activated!"
    echo "📁 Current directory: $(pwd)"
    echo "🐍 Python: $(which python)"
    echo "✅ Django check: $(python manage.py check --quiet && echo 'PASSED' || echo 'FAILED')"
    echo ""
    echo "🎯 Common commands:"
    echo "   python manage.py runserver      # Start server"
    echo "   python manage.py migrate        # Run migrations"
    echo "   python manage.py shell          # Django shell"
    echo ""
    exec bash
else
    echo "🚀 Running: $@"
    exec "$@"
fi
