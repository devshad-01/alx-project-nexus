#!/usr/bin/env python3
"""
Quick Registration Test
"""

import requests
import json
from datetime import datetime

def test_registration():
    url = "http://localhost:8000/api/auth/register/"
    
    data = {
        'email': f'testuser_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
        'password': 'TestPassword123!',
        'password_confirm': 'TestPassword123!',
        'first_name': 'Test',
        'last_name': 'User'
    }
    
    try:
        response = requests.post(url, json=data, headers={'Content-Type': 'application/json'})
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ Registration successful!")
            result = response.json()
            print(f"Access Token: {result.get('tokens', {}).get('access', 'NOT FOUND')[:50]}...")
        else:
            print("❌ Registration failed")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_registration()
