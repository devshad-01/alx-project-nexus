#!/bin/bash

# ALX Project Nexus - Quick Commands Setup
# This creates aliases for easier development

PROJECT_ROOT="/home/shad/Desktop/alx_project_nexus"
BACKEND_DIR="$PROJECT_ROOT/ecommerce_backend"
VENV_PYTHON="$BACKEND_DIR/venv/bin/python"
VENV_PIP="$BACKEND_DIR/venv/bin/pip"

# Create aliases for easier development
alias alx-cd="cd $BACKEND_DIR"
alias alx-python="$VENV_PYTHON"
alias alx-pip="$VENV_PIP"
alias alx-manage="$VENV_PYTHON $BACKEND_DIR/manage.py"
alias alx-server="$VENV_PYTHON $BACKEND_DIR/manage.py runserver"
alias alx-shell="$VENV_PYTHON $BACKEND_DIR/manage.py shell"
alias alx-migrate="$VENV_PYTHON $BACKEND_DIR/manage.py migrate"
alias alx-check="$VENV_PYTHON $BACKEND_DIR/manage.py check"

echo "🎯 ALX Project Aliases Created!"
echo "================================"
echo "Available commands:"
echo "  alx-cd        # Change to backend directory"
echo "  alx-python    # Run Python in virtual environment"
echo "  alx-pip       # Run pip in virtual environment"
echo "  alx-manage    # Run Django manage.py commands"
echo "  alx-server    # Start development server"
echo "  alx-shell     # Open Django shell"
echo "  alx-migrate   # Run database migrations"
echo "  alx-check     # Check for Django issues"
echo "================================"
echo ""
echo "Example usage:"
echo "  alx-cd && alx-server"
echo "  alx-manage createsuperuser"
echo "  alx-pip install package-name"
