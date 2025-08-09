#!/usr/bin/env python3
"""
Comprehensive API Testing Script for ALX Project Nexus E-Commerce Backend
Tests all endpoints with proper authentication and error handling
"""

import requests
import json
import sys
from typing import Dict, Any, Optional

class APITester:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None
        self.refresh_token = None
        self.test_user_id = None
        self.test_category_id = None
        self.test_product_id = None
        self.test_order_id = None
        
        # Test counters
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0

    def log(self, message: str, level: str = "INFO"):
        """Log messages with formatting"""
        colors = {
            "INFO": "\033[94m",
            "SUCCESS": "\033[92m", 
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "RESET": "\033[0m"
        }
        print(f"{colors.get(level, colors['INFO'])}[{level}] {message}{colors['RESET']}")

    def make_request(self, method: str, endpoint: str, data: Dict = None, 
                    auth: bool = True, expected_status: int = None) -> requests.Response:
        """Make HTTP request with proper headers"""
        url = f"{self.base_url}{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if auth and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                response = self.session.post(url, json=data, headers=headers)
            elif method.upper() == "PUT":
                response = self.session.put(url, json=data, headers=headers)
            elif method.upper() == "PATCH":
                response = self.session.patch(url, json=data, headers=headers)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
                
            return response
        except requests.exceptions.RequestException as e:
            self.log(f"Request failed: {e}", "ERROR")
            return None

    def test_endpoint(self, name: str, method: str, endpoint: str, 
                     data: Dict = None, auth: bool = True, 
                     expected_status: int = 200) -> Dict[str, Any]:
        """Test a single endpoint"""
        self.total_tests += 1
        
        self.log(f"Testing {name}: {method.upper()} {endpoint}")
        
        response = self.make_request(method, endpoint, data, auth, expected_status)
        
        if response is None:
            self.failed_tests += 1
            self.log(f"❌ {name} - Request failed", "ERROR")
            return {"success": False, "error": "Request failed"}
        
        success = response.status_code == expected_status
        
        if success:
            self.passed_tests += 1
            self.log(f"✅ {name} - Status: {response.status_code}", "SUCCESS")
        else:
            self.failed_tests += 1
            self.log(f"❌ {name} - Expected: {expected_status}, Got: {response.status_code}", "ERROR")
            try:
                error_detail = response.json()
                self.log(f"Error details: {json.dumps(error_detail, indent=2)}", "ERROR")
            except:
                self.log(f"Response text: {response.text[:200]}...", "ERROR")
        
        try:
            response_data = response.json() if response.content else {}
        except:
            response_data = {"raw_response": response.text}
        
        return {
            "success": success,
            "status_code": response.status_code,
            "data": response_data,
            "response": response
        }

    def test_authentication_endpoints(self):
        """Test all authentication-related endpoints"""
        self.log("\n🔐 TESTING AUTHENTICATION ENDPOINTS", "INFO")
        
        # Test user registration
        register_data = {
            "username": "testuser123",
            "email": "testuser123@example.com",
            "password": "TestPassword123!",
            "password_confirm": "TestPassword123!",
            "first_name": "Test",
            "last_name": "User"
        }
        
        result = self.test_endpoint(
            "User Registration",
            "POST",
            "/api/auth/register/",
            register_data,
            auth=False,
            expected_status=201
        )
        
        if result["success"]:
            self.test_user_id = result["data"].get("id")
            self.log(f"Created test user with ID: {self.test_user_id}")
        
        # Test user login
        login_data = {
            "email": "testuser123@example.com",
            "password": "TestPassword123!"
        }
        
        result = self.test_endpoint(
            "User Login",
            "POST", 
            "/api/auth/login/",
            login_data,
            auth=False
        )
        
        if result["success"]:
            self.access_token = result["data"].get("access")
            self.refresh_token = result["data"].get("refresh")
            self.log(f"Obtained access token: {self.access_token[:20]}...")
        
        # Test token refresh
        if self.refresh_token:
            refresh_data = {"refresh": self.refresh_token}
            self.test_endpoint(
                "Token Refresh",
                "POST",
                "/api/auth/refresh/",
                refresh_data,
                auth=False
            )
        
        # Test get profile
        self.test_endpoint(
            "Get User Profile",
            "GET",
            "/api/auth/profile/"
        )
        
        # Test update profile
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": "testuser123@example.com"
        }
        
        self.test_endpoint(
            "Update User Profile",
            "PUT",
            "/api/auth/profile/update/",
            update_data
        )
        
        # Test auth status
        self.test_endpoint(
            "Authentication Status",
            "GET",
            "/api/auth/status/"
        )

    def test_product_endpoints(self):
        """Test product and category endpoints"""
        self.log("\n🛍️ TESTING PRODUCT ENDPOINTS", "INFO")
        
        # Test create category (admin required)
        category_data = {
            "name": "Test Electronics",
            "description": "Test category for electronics",
            "is_active": True
        }
        
        result = self.test_endpoint(
            "Create Category",
            "POST",
            "/api/products/categories/",
            category_data
        )
        
        if result["success"]:
            self.test_category_id = result["data"].get("id")
            self.log(f"Created test category with ID: {self.test_category_id}")
        
        # Test list categories (public)
        self.test_endpoint(
            "List Categories",
            "GET",
            "/api/products/categories/",
            auth=False
        )
        
        # Test list products (public)
        self.test_endpoint(
            "List Products",
            "GET",
            "/api/products/",
            auth=False
        )
        
        # Test create product
        if self.test_category_id:
            product_data = {
                "name": "Test Smartphone",
                "description": "A test smartphone product",
                "price": "599.99",
                "category": self.test_category_id,
                "sku": "TEST-PHONE-001",
                "stock_quantity": 50,
                "is_active": True,
                "is_featured": True
            }
            
            result = self.test_endpoint(
                "Create Product",
                "POST",
                "/api/products/",
                product_data
            )
            
            if result["success"]:
                self.test_product_id = result["data"].get("id")
                self.log(f"Created test product with ID: {self.test_product_id}")
        
        # Test get product detail
        if self.test_product_id:
            self.test_endpoint(
                "Get Product Detail",
                "GET",
                f"/api/products/{self.test_product_id}/",
                auth=False
            )
            
            # Test update product
            update_data = {
                "name": "Updated Test Smartphone",
                "price": "649.99",
                "stock_quantity": 45
            }
            
            self.test_endpoint(
                "Update Product",
                "PATCH",
                f"/api/products/{self.test_product_id}/",
                update_data
            )

    def test_cart_endpoints(self):
        """Test shopping cart endpoints"""
        self.log("\n🛒 TESTING CART ENDPOINTS", "INFO")
        
        # Test get cart
        self.test_endpoint(
            "Get Shopping Cart",
            "GET",
            "/api/cart/"
        )
        
        # Test add item to cart
        if self.test_product_id:
            cart_item_data = {
                "product": self.test_product_id,
                "quantity": 2
            }
            
            self.test_endpoint(
                "Add Item to Cart",
                "POST",
                "/api/cart/add/",
                cart_item_data
            )
            
            # Test update cart item
            update_data = {"quantity": 3}
            self.test_endpoint(
                "Update Cart Item",
                "PATCH",
                f"/api/cart/items/{self.test_product_id}/",
                update_data
            )
        
        # Test clear cart
        self.test_endpoint(
            "Clear Cart",
            "DELETE",
            "/api/cart/clear/"
        )

    def test_order_endpoints(self):
        """Test order management endpoints"""
        self.log("\n📦 TESTING ORDER ENDPOINTS", "INFO")
        
        # First add item to cart for order creation
        if self.test_product_id:
            cart_item_data = {
                "product": self.test_product_id,
                "quantity": 1
            }
            
            self.test_endpoint(
                "Add Item for Order",
                "POST",
                "/api/cart/add/",
                cart_item_data
            )
        
        # Test create order
        order_data = {
            "shipping_address": {
                "street": "123 Test Street",
                "city": "Test City", 
                "state": "Test State",
                "postal_code": "12345",
                "country": "Test Country"
            },
            "payment_method": "credit_card",
            "notes": "Test order"
        }
        
        result = self.test_endpoint(
            "Create Order from Cart",
            "POST",
            "/api/orders/create-from-cart/",
            order_data
        )
        
        if result["success"]:
            self.test_order_id = result["data"].get("id")
            self.log(f"Created test order with ID: {self.test_order_id}")
        
        # Test list orders
        self.test_endpoint(
            "List User Orders",
            "GET",
            "/api/orders/"
        )
        
        # Test get order detail
        if self.test_order_id:
            self.test_endpoint(
                "Get Order Detail",
                "GET",
                f"/api/orders/{self.test_order_id}/"
            )
            
            # Test update order status
            status_data = {"status": "confirmed"}
            self.test_endpoint(
                "Update Order Status",
                "PATCH",
                f"/api/orders/{self.test_order_id}/",
                status_data
            )

    def test_review_endpoints(self):
        """Test product review endpoints"""
        self.log("\n⭐ TESTING REVIEW ENDPOINTS", "INFO")
        
        if self.test_product_id:
            # Test create review
            review_data = {
                "product": self.test_product_id,
                "rating": 5,
                "title": "Great product!",
                "comment": "This is an excellent product. Highly recommended!"
            }
            
            self.test_endpoint(
                "Create Product Review",
                "POST",
                "/api/reviews/",
                review_data
            )
            
            # Test list product reviews
            self.test_endpoint(
                "List Product Reviews",
                "GET",
                f"/api/products/{self.test_product_id}/reviews/",
                auth=False
            )

    def test_api_documentation(self):
        """Test API documentation endpoints"""
        self.log("\n📚 TESTING API DOCUMENTATION", "INFO")
        
        # Test OpenAPI schema
        self.test_endpoint(
            "API Schema",
            "GET",
            "/api/schema/",
            auth=False
        )
        
        # Test Swagger UI
        result = self.test_endpoint(
            "Swagger UI",
            "GET",
            "/api/docs/",
            auth=False
        )
        
        # Check if response contains HTML
        if result["success"] and "swagger" in result.get("response", {}).text.lower():
            self.log("✅ Swagger UI is properly loaded", "SUCCESS")
        
        # Test ReDoc
        result = self.test_endpoint(
            "ReDoc Documentation",
            "GET",
            "/api/redoc/",
            auth=False
        )
        
        # Check if response contains HTML
        if result["success"] and "redoc" in result.get("response", {}).text.lower():
            self.log("✅ ReDoc is properly loaded", "SUCCESS")

    def test_error_handling(self):
        """Test error handling and edge cases"""
        self.log("\n🚨 TESTING ERROR HANDLING", "INFO")
        
        # Test 404 endpoint
        self.test_endpoint(
            "Non-existent Endpoint",
            "GET",
            "/api/nonexistent/",
            auth=False,
            expected_status=404
        )
        
        # Test unauthorized access
        self.test_endpoint(
            "Unauthorized Access",
            "GET",
            "/api/auth/profile/",
            auth=False,
            expected_status=401
        )
        
        # Test invalid data
        invalid_data = {
            "email": "invalid-email",
            "password": "123"
        }
        
        self.test_endpoint(
            "Invalid Registration Data",
            "POST",
            "/api/auth/register/",
            invalid_data,
            auth=False,
            expected_status=400
        )

    def cleanup(self):
        """Clean up test data"""
        self.log("\n🧹 CLEANING UP TEST DATA", "INFO")
        
        # Delete test product
        if self.test_product_id:
            self.test_endpoint(
                "Delete Test Product",
                "DELETE",
                f"/api/products/{self.test_product_id}/"
            )
        
        # Delete test category  
        if self.test_category_id:
            self.test_endpoint(
                "Delete Test Category",
                "DELETE",
                f"/api/products/categories/{self.test_category_id}/"
            )

    def run_all_tests(self):
        """Run comprehensive API test suite"""
        self.log("🚀 STARTING COMPREHENSIVE API TESTING", "INFO")
        self.log("=" * 60, "INFO")
        
        try:
            # Run test suites
            self.test_authentication_endpoints()
            self.test_product_endpoints()
            self.test_cart_endpoints()
            self.test_order_endpoints()
            self.test_review_endpoints()
            self.test_api_documentation()
            self.test_error_handling()
            
            # Clean up
            self.cleanup()
            
        except KeyboardInterrupt:
            self.log("\n⚠️ Testing interrupted by user", "WARNING")
        except Exception as e:
            self.log(f"\n💥 Testing failed with error: {e}", "ERROR")
        
        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print test execution summary"""
        self.log("\n" + "=" * 60, "INFO")
        self.log("📊 TEST EXECUTION SUMMARY", "INFO")
        self.log("=" * 60, "INFO")
        
        self.log(f"Total Tests: {self.total_tests}")
        self.log(f"Passed: {self.passed_tests}", "SUCCESS")
        self.log(f"Failed: {self.failed_tests}", "ERROR")
        
        if self.failed_tests == 0:
            self.log("🎉 ALL TESTS PASSED!", "SUCCESS")
            success_rate = 100.0
        else:
            success_rate = (self.passed_tests / self.total_tests) * 100
            self.log(f"⚠️ {self.failed_tests} tests failed", "WARNING")
        
        self.log(f"Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 90:
            self.log("✅ API is working excellently!", "SUCCESS")
        elif success_rate >= 75:
            self.log("⚠️ API has minor issues", "WARNING")
        else:
            self.log("❌ API has significant issues that need attention", "ERROR")


def main():
    """Main function to run API tests"""
    # Check if server is running
    try:
        response = requests.get("http://localhost:8000/api/schema/", timeout=5)
        if response.status_code != 200:
            print("❌ Django server is not responding properly")
            sys.exit(1)
    except requests.exceptions.RequestException:
        print("❌ Cannot connect to Django server at http://localhost:8000")
        print("Please make sure the server is running with: python manage.py runserver")
        sys.exit(1)
    
    # Run tests
    tester = APITester()
    tester.run_all_tests()


if __name__ == "__main__":
    main()
