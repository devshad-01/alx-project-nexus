#!/usr/bin/env python3
"""
Comprehensive API Testing Script for ALX Project Nexus E-commerce Backend

This script performs thorough testing of all API endpoints to ensure they work correctly.
"""

import requests
import json
import sys
from datetime import datetime
from typing import Dict, Any, List, Optional


class APITester:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = requests.Session()
        self.auth_token = None
        self.admin_token = None
        self.test_user_id = None
        self.test_product_id = None
        self.test_category_id = None
        self.test_order_id = None
        self.test_results = []
        
    def log_test(self, endpoint: str, method: str, status: str, details: str = ""):
        """Log test results"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = {
            'timestamp': timestamp,
            'endpoint': endpoint,
            'method': method,
            'status': status,
            'details': details
        }
        self.test_results.append(result)
        
        status_emoji = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_emoji} [{timestamp}] {method} {endpoint} - {status}")
        if details:
            print(f"    {details}")
    
    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    headers: Dict = None, auth_required: bool = False) -> requests.Response:
        """Make HTTP request with proper headers"""
        url = f"{self.base_url}{endpoint}"
        
        # Prepare headers
        request_headers = {'Content-Type': 'application/json'}
        if headers:
            request_headers.update(headers)
        
        # Add authentication if required
        if auth_required and self.auth_token:
            request_headers['Authorization'] = f'Bearer {self.auth_token}'
        
        # Make request
        try:
            if method.upper() == 'GET':
                response = self.session.get(url, headers=request_headers)
            elif method.upper() == 'POST':
                response = self.session.post(url, json=data, headers=request_headers)
            elif method.upper() == 'PUT':
                response = self.session.put(url, json=data, headers=request_headers)
            elif method.upper() == 'PATCH':
                response = self.session.patch(url, json=data, headers=request_headers)
            elif method.upper() == 'DELETE':
                response = self.session.delete(url, headers=request_headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            
            return response
        except Exception as e:
            raise Exception(f"Request failed: {str(e)}")
    
    def test_api_schema(self):
        """Test API schema endpoints"""
        print("\n📊 Testing API Schema Endpoints...")
        
        endpoints = [
            ('/schema/', 'GET'),
            ('/docs/', 'GET'),
            ('/redoc/', 'GET'),
        ]
        
        for endpoint, method in endpoints:
            try:
                response = self.make_request(method, endpoint)
                if response.status_code == 200:
                    self.log_test(endpoint, method, "PASS", 
                                f"Status: {response.status_code}")
                else:
                    self.log_test(endpoint, method, "FAIL", 
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(endpoint, method, "FAIL", str(e))
    
    def test_authentication(self):
        """Test authentication endpoints"""
        print("\n🔐 Testing Authentication Endpoints...")
        
        # Test user registration
        registration_data = {
            'email': f'testuser_{datetime.now().strftime("%Y%m%d_%H%M%S")}@example.com',
            'password': 'TestPassword123!',
            'password_confirm': 'TestPassword123!',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        try:
            response = self.make_request('POST', '/auth/register/', registration_data)
            if response.status_code == 201:
                data = response.json()
                self.auth_token = data.get('tokens', {}).get('access')
                self.test_user_id = data.get('user', {}).get('id')
                self.log_test('/auth/register/', 'POST', "PASS", 
                            f"User registered successfully. Token received: {'Yes' if self.auth_token else 'No'}")
            else:
                self.log_test('/auth/register/', 'POST', "FAIL", 
                            f"Status: {response.status_code}, Response: {response.text}")
        except Exception as e:
            self.log_test('/auth/register/', 'POST', "FAIL", str(e))
        
        # Test login with the registered user
        if self.auth_token:
            login_data = {
                'email': registration_data['email'],
                'password': registration_data['password']
            }
            
            try:
                response = self.make_request('POST', '/auth/login/', login_data)
                if response.status_code == 200:
                    self.log_test('/auth/login/', 'POST', "PASS", 
                                f"Login successful")
                else:
                    self.log_test('/auth/login/', 'POST', "FAIL", 
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test('/auth/login/', 'POST', "FAIL", str(e))
        
        # Test profile endpoint
        if self.auth_token:
            try:
                response = self.make_request('GET', '/auth/profile/', auth_required=True)
                if response.status_code == 200:
                    self.log_test('/auth/profile/', 'GET', "PASS", 
                                "Profile retrieved successfully")
                else:
                    self.log_test('/auth/profile/', 'GET', "FAIL", 
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test('/auth/profile/', 'GET', "FAIL", str(e))
    
    def test_products(self):
        """Test product endpoints"""
        print("\n📦 Testing Product Endpoints...")
        
        # Test categories list (public)
        try:
            response = self.make_request('GET', '/products/categories/')
            if response.status_code == 200:
                self.log_test('/products/categories/', 'GET', "PASS", 
                            f"Categories retrieved. Count: {len(response.json())}")
            else:
                self.log_test('/products/categories/', 'GET', "FAIL", 
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('/products/categories/', 'GET', "FAIL", str(e))
        
        # Test products list (public)
        try:
            response = self.make_request('GET', '/products/')
            if response.status_code == 200:
                data = response.json()
                product_count = len(data.get('results', [])) if 'results' in data else len(data)
                self.log_test('/products/', 'GET', "PASS", 
                            f"Products retrieved. Count: {product_count}")
                
                # Store a product ID for further testing
                if 'results' in data and data['results']:
                    self.test_product_id = data['results'][0].get('id')
                elif isinstance(data, list) and data:
                    self.test_product_id = data[0].get('id')
            else:
                self.log_test('/products/', 'GET', "FAIL", 
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('/products/', 'GET', "FAIL", str(e))
        
        # Test product detail if we have a product ID
        if self.test_product_id:
            try:
                response = self.make_request('GET', f'/products/{self.test_product_id}/')
                if response.status_code == 200:
                    self.log_test(f'/products/{self.test_product_id}/', 'GET', "PASS", 
                                "Product detail retrieved")
                else:
                    self.log_test(f'/products/{self.test_product_id}/', 'GET', "FAIL", 
                                f"Status: {response.status_code}")
            except Exception as e:
                self.log_test(f'/products/{self.test_product_id}/', 'GET', "FAIL", str(e))
        else:
            self.log_test('/products/<id>/', 'GET', "SKIP", "No product ID available for testing")
    
    def test_cart_operations(self):
        """Test cart operations"""
        print("\n🛒 Testing Cart Operations...")
        
        if not self.auth_token:
            self.log_test('/cart/', 'GET', "SKIP", "No auth token available")
            return
        
        # Test get cart
        try:
            response = self.make_request('GET', '/cart/', auth_required=True)
            if response.status_code == 200:
                self.log_test('/cart/', 'GET', "PASS", 
                            "Cart retrieved successfully")
            else:
                self.log_test('/cart/', 'GET', "FAIL", 
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('/cart/', 'GET', "FAIL", str(e))
        
        # Test add to cart (if we have a product)
        if self.test_product_id:
            cart_item_data = {
                'product': self.test_product_id,
                'quantity': 2
            }
            
            try:
                response = self.make_request('POST', '/cart/add/', 
                                          cart_item_data, auth_required=True)
                if response.status_code in [200, 201]:
                    self.log_test('/cart/add/', 'POST', "PASS", 
                                "Item added to cart")
                else:
                    self.log_test('/cart/add/', 'POST', "FAIL", 
                                f"Status: {response.status_code}, Response: {response.text}")
            except Exception as e:
                self.log_test('/cart/add/', 'POST', "FAIL", str(e))
    
    def test_orders(self):
        """Test order operations"""
        print("\n📋 Testing Order Operations...")
        
        if not self.auth_token:
            self.log_test('/orders/', 'GET', "SKIP", "No auth token available")
            return
        
        # Test orders list
        try:
            response = self.make_request('GET', '/orders/', auth_required=True)
            if response.status_code == 200:
                self.log_test('/orders/', 'GET', "PASS", 
                            "Orders retrieved successfully")
            else:
                self.log_test('/orders/', 'GET', "FAIL", 
                            f"Status: {response.status_code}")
        except Exception as e:
            self.log_test('/orders/', 'GET', "FAIL", str(e))
    
    def test_error_handling(self):
        """Test error handling for invalid endpoints"""
        print("\n❌ Testing Error Handling...")
        
        # Test 404 for non-existent endpoint
        try:
            response = self.make_request('GET', '/non-existent-endpoint/')
            if response.status_code == 404:
                self.log_test('/non-existent-endpoint/', 'GET', "PASS", 
                            "404 error handled correctly")
            else:
                self.log_test('/non-existent-endpoint/', 'GET', "FAIL", 
                            f"Expected 404, got {response.status_code}")
        except Exception as e:
            self.log_test('/non-existent-endpoint/', 'GET', "FAIL", str(e))
        
        # Test 401 for protected endpoint without auth
        try:
            response = self.make_request('GET', '/auth/profile/')
            if response.status_code == 401:
                self.log_test('/auth/profile/ (no auth)', 'GET', "PASS", 
                            "401 unauthorized handled correctly")
            else:
                self.log_test('/auth/profile/ (no auth)', 'GET', "FAIL", 
                            f"Expected 401, got {response.status_code}")
        except Exception as e:
            self.log_test('/auth/profile/ (no auth)', 'GET', "FAIL", str(e))
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Comprehensive API Testing...")
        print(f"📡 Testing against: {self.base_url}")
        print("=" * 60)
        
        # Run all test suites
        self.test_api_schema()
        self.test_authentication()
        self.test_products()
        self.test_cart_operations()
        self.test_orders()
        self.test_error_handling()
        
        # Print summary
        self.print_summary()
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = len([r for r in self.test_results if r['status'] == 'PASS'])
        failed_tests = len([r for r in self.test_results if r['status'] == 'FAIL'])
        skipped_tests = len([r for r in self.test_results if r['status'] == 'SKIP'])
        
        print(f"Total Tests: {total_tests}")
        print(f"✅ Passed: {passed_tests}")
        print(f"❌ Failed: {failed_tests}")
        print(f"⚠️  Skipped: {skipped_tests}")
        
        success_rate = (passed_tests / total_tests * 100) if total_tests > 0 else 0
        print(f"\n📈 Success Rate: {success_rate:.1f}%")
        
        if failed_tests > 0:
            print(f"\n❌ Failed Tests:")
            for result in self.test_results:
                if result['status'] == 'FAIL':
                    print(f"   - {result['method']} {result['endpoint']}: {result['details']}")
        
        # Save detailed results to file
        self.save_results_to_file()
        
        print(f"\n📄 Detailed results saved to: api_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
    
    def save_results_to_file(self):
        """Save test results to JSON file"""
        filename = f"api_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        summary = {
            'test_run': {
                'timestamp': datetime.now().isoformat(),
                'base_url': self.base_url,
                'total_tests': len(self.test_results),
                'passed': len([r for r in self.test_results if r['status'] == 'PASS']),
                'failed': len([r for r in self.test_results if r['status'] == 'FAIL']),
                'skipped': len([r for r in self.test_results if r['status'] == 'SKIP']),
            },
            'test_results': self.test_results
        }
        
        with open(filename, 'w') as f:
            json.dump(summary, f, indent=2)


def main():
    """Main function"""
    # Check if server is running
    tester = APITester()
    
    try:
        response = tester.make_request('GET', '/schema/')
        if response.status_code != 200:
            print("❌ Server doesn't seem to be running on http://localhost:8000")
            print("   Please start the Django server with: python manage.py runserver")
            sys.exit(1)
    except Exception as e:
        print("❌ Cannot connect to server on http://localhost:8000")
        print(f"   Error: {e}")
        print("   Please start the Django server with: python manage.py runserver")
        sys.exit(1)
    
    # Run tests
    tester.run_all_tests()


if __name__ == "__main__":
    main()
