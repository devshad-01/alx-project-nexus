#!/usr/bin/env python3
"""
Quick test script to verify admin login functionality
"""
import requests
import json
from datetime import datetime

def test_admin_access():
    """Test admin login without CSRF"""
    base_url = "https://alx-project-nexus-nb67.onrender.com"
    admin_login_url = f"{base_url}/admin/login/"
    
    print(f"Testing admin access at: {admin_login_url}")
    print(f"Time: {datetime.now()}")
    print("-" * 50)
    
    # Test 1: Check if admin login page loads
    try:
        response = requests.get(admin_login_url)
        print(f"✓ Admin login page status: {response.status_code}")
        if response.status_code == 200:
            print("✓ Admin login page loads successfully")
        else:
            print(f"✗ Admin login page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error accessing admin page: {e}")
        return False
    
    # Test 2: Attempt login (this will fail with CSRF but we can see the error)
    login_data = {
        'username': 'admin',
        'password': 'Admin123!',
        'next': '/admin/'
    }
    
    try:
        # Create a session to maintain cookies
        session = requests.Session()
        
        # Get the login page first to get any cookies/session
        login_page = session.get(admin_login_url)
        print(f"✓ Login page cookies received: {len(session.cookies)}")
        
        # Try to login (without CSRF token for now)
        login_response = session.post(admin_login_url, data=login_data)
        print(f"Login attempt status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            print("✓ Login successful or redirected!")
            return True
        elif login_response.status_code == 302:
            print("✓ Login redirect (likely successful)!")
            print(f"Redirect location: {login_response.headers.get('Location', 'Unknown')}")
            return True
        elif login_response.status_code == 400:
            print("✗ Bad Request (400) - likely CSRF issue")
            return False
        else:
            print(f"✗ Unexpected status: {login_response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error during login attempt: {e}")
        return False

if __name__ == "__main__":
    test_admin_access()
