#!/usr/bin/env python3
"""
Comprehensive API Testing Script for ALX Project Nexus E-Commerce Backend
Tests all API endpoints systematically to ensure functionality
"""

import requests
import json
import sys
from datetime import datetime
import time

class APITester:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url
        self.api_url = f"{base_url}/api"
        self.access_token = None
        self.refresh_token = None
        self.test_user_id = None
        self.test_category_id = None
        self.test_product_id = None
        self.test_order_id = None
        
        # Test data
        self.test_user = {
            "username": f"testuser_{int(time.time())}",
            "email": f"test_{int(time.time())}@example.com",
            "password": "testpass123",
            "password_confirm": "testpass123",
            "first_name": "Test",
            "last_name": "User"
        }
        
        self.test_category = {
            "name": f"Test Category {int(time.time())}",
            "description": "Test category for API testing",
            "is_active": True
        }
        
        self.test_product = {
            "name": f"Test Product {int(time.time())}",
            "description": "Test product for API testing",
            "price": "99.99",
            "sku": f"TEST-{int(time.time())}",
            "stock_quantity": 100,
            "is_active": True,
            "is_featured": False
        }
        
        self.results = []
    
    def log(self, message, status="INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {status}: {message}")
        self.results.append({"timestamp": timestamp, "status": status, "message": message})
    
    def make_request(self, method, endpoint, data=None, headers=None, auth_required=True):
        """Make HTTP request with optional authentication"""
        url = f"{self.api_url}{endpoint}"
        
        # Default headers
        req_headers = {"Content-Type": "application/json"}
        if headers:
            req_headers.update(headers)
        
        # Add auth header if token available and required
        if auth_required and self.access_token:
            req_headers["Authorization"] = f"Bearer {self.access_token}"
        
        try:
            if method.upper() == "GET":
                response = requests.get(url, headers=req_headers)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=req_headers)
            elif method.upper() == "PUT":
                response = requests.put(url, json=data, headers=req_headers)
            elif method.upper() == "PATCH":
                response = requests.patch(url, json=data, headers=req_headers)
            elif method.upper() == "DELETE":
                response = requests.delete(url, headers=req_headers)
            else:
                raise ValueError(f"Unsupported method: {method}")
            
            return response
        except requests.exceptions.RequestException as e:
            self.log(f"Request failed: {e}", "ERROR")
            return None
    
    def test_endpoint(self, name, method, endpoint, data=None, expected_status=200, auth_required=True):
        """Test a single endpoint"""
        self.log(f"Testing {name}: {method} {endpoint}")
        
        response = self.make_request(method, endpoint, data, auth_required=auth_required)
        if not response:
            self.log(f"❌ {name} - Request failed", "ERROR")
            return None
        
        if response.status_code == expected_status:
            self.log(f"✅ {name} - Status: {response.status_code}", "SUCCESS")
            try:
                return response.json() if response.content else None
            except:
                return response.text
        else:
            self.log(f"❌ {name} - Expected {expected_status}, got {response.status_code}", "ERROR")
            try:
                error_detail = response.json()
                self.log(f"Error details: {error_detail}", "ERROR")
            except:
                self.log(f"Error response: {response.text}", "ERROR")
            return None
    
    def test_authentication(self):
        """Test authentication endpoints"""
        self.log("🔐 Testing Authentication Endpoints", "HEADER")
        
        # 1. Test user registration
        result = self.test_endpoint(
            "User Registration",
            "POST",
            "/auth/register/",
            self.test_user,
            201,
            auth_required=False
        )
        
        if result:
            self.test_user_id = result.get("id")
            self.log(f"User created with ID: {self.test_user_id}")
        
        # 2. Test user login
        login_data = {
            "email": self.test_user["email"],
            "password": self.test_user["password"]
        }
        
        result = self.test_endpoint(
            "User Login",
            "POST",
            "/auth/login/",
            login_data,
            200,
            auth_required=False
        )
        
        if result:
            self.access_token = result.get("access")
            self.refresh_token = result.get("refresh")
            self.log("Login successful, tokens obtained")
        
        # 3. Test profile retrieval
        self.test_endpoint(
            "Get User Profile",
            "GET",
            "/auth/profile/",
            expected_status=200
        )
        
        # 4. Test profile update
        update_data = {
            "first_name": "Updated",
            "last_name": "Name",
            "email": self.test_user["email"]
        }
        
        self.test_endpoint(
            "Update User Profile",
            "PUT",
            "/auth/profile/update/",
            update_data,
            200
        )
        
        # 5. Test token refresh
        if self.refresh_token:
            refresh_data = {"refresh": self.refresh_token}
            result = self.test_endpoint(
                "Token Refresh",
                "POST",
                "/auth/refresh/",
                refresh_data,
                200,
                auth_required=False
            )
            
            if result:
                self.access_token = result.get("access")
                self.log("Token refreshed successfully")
        
        # 6. Test auth status
        self.test_endpoint(
            "Auth Status Check",
            "GET",
            "/auth/status/",
            expected_status=200
        )
    
    def test_categories(self):
        """Test category endpoints"""
        self.log("📦 Testing Category Endpoints", "HEADER")
        
        # 1. Create category
        result = self.test_endpoint(
            "Create Category",
            "POST",
            "/products/categories/",
            self.test_category,
            201
        )
        
        if result:
            self.test_category_id = result.get("id")
            self.test_category_slug = result.get("slug")
            self.log(f"Category created with ID: {self.test_category_id}")
        
        # 2. List categories (public)
        self.test_endpoint(
            "List Categories",
            "GET",
            "/products/categories/",
            expected_status=200,
            auth_required=False
        )
        
        # 3. Get category detail
        if self.test_category_slug:
            self.test_endpoint(
                "Get Category Detail",
                "GET",
                f"/products/categories/{self.test_category_slug}/",
                expected_status=200,
                auth_required=False
            )
            
            # 4. Update category
            update_data = {
                "name": f"Updated {self.test_category['name']}",
                "description": "Updated description"
            }
            
            self.test_endpoint(
                "Update Category",
                "PUT",
                f"/products/categories/{self.test_category_slug}/",
                update_data,
                200
            )
    
    def test_products(self):
        """Test product endpoints"""
        self.log("🛍️ Testing Product Endpoints", "HEADER")
        
        # Add category to product data
        if self.test_category_id:
            self.test_product["category"] = self.test_category_id
        
        # 1. Create product
        result = self.test_endpoint(
            "Create Product",
            "POST",
            "/products/",
            self.test_product,
            201
        )
        
        if result:
            self.test_product_id = result.get("id")
            self.test_product_slug = result.get("slug")
            self.log(f"Product created with ID: {self.test_product_id}")
        
        # 2. List products (public)
        self.test_endpoint(
            "List Products",
            "GET",
            "/products/",
            expected_status=200,
            auth_required=False
        )
        
        # 3. Get product detail
        if self.test_product_slug:
            self.test_endpoint(
                "Get Product Detail",
                "GET",
                f"/products/{self.test_product_slug}/",
                expected_status=200,
                auth_required=False
            )
            
            # 4. Update product
            update_data = {
                "name": f"Updated {self.test_product['name']}",
                "price": "149.99",
                "stock_quantity": 50,
                "category": self.test_category_id
            }
            
            self.test_endpoint(
                "Update Product",
                "PUT",
                f"/products/{self.test_product_slug}/",
                update_data,
                200
            )
            
            # 5. Test product reviews
            review_data = {
                "product": self.test_product_id,
                "rating": 5,
                "title": "Great product!",
                "comment": "Really love this test product."
            }
            
            self.test_endpoint(
                "Create Product Review",
                "POST",
                f"/products/{self.test_product_slug}/reviews/",
                review_data,
                201
            )
            
            # 6. List product reviews
            self.test_endpoint(
                "List Product Reviews",
                "GET",
                f"/products/{self.test_product_slug}/reviews/",
                expected_status=200,
                auth_required=False
            )
    
    def test_cart(self):
        """Test shopping cart endpoints"""
        self.log("🛒 Testing Cart Endpoints", "HEADER")
        
        # 1. Get cart (should be empty initially)
        self.test_endpoint(
            "Get Cart",
            "GET",
            "/cart/",
            expected_status=200
        )
        
        # 2. Add item to cart
        if self.test_product_id:
            add_data = {
                "product": self.test_product_id,
                "quantity": 2
            }
            
            result = self.test_endpoint(
                "Add Item to Cart",
                "POST",
                "/cart/add/",
                add_data,
                201
            )
            
            cart_item_id = None
            if result:
                cart_item_id = result.get("id")
                self.log(f"Item added to cart with ID: {cart_item_id}")
            
            # 3. Get cart with items
            self.test_endpoint(
                "Get Cart with Items",
                "GET",
                "/cart/",
                expected_status=200
            )
            
            # 4. Update cart item
            if cart_item_id:
                update_data = {"quantity": 3}
                
                self.test_endpoint(
                    "Update Cart Item",
                    "PATCH",
                    f"/cart/update/{cart_item_id}/",
                    update_data,
                    200
                )
                
                # 5. Remove cart item
                self.test_endpoint(
                    "Remove Cart Item",
                    "DELETE",
                    f"/cart/remove/{cart_item_id}/",
                    expected_status=204
                )
        
        # 6. Clear cart
        self.test_endpoint(
            "Clear Cart",
            "DELETE",
            "/cart/clear/",
            expected_status=204
        )
    
    def test_orders(self):
        """Test order endpoints"""
        self.log("📋 Testing Order Endpoints", "HEADER")
        
        # First, add item to cart for order creation
        if self.test_product_id:
            add_data = {
                "product": self.test_product_id,
                "quantity": 1
            }
            
            self.test_endpoint(
                "Add Item for Order",
                "POST",
                "/cart/add/",
                add_data,
                201
            )
        
        # 1. Create order
        order_data = {
            "shipping_address": {
                "street": "123 Test St",
                "city": "Test City",
                "state": "TS",
                "zip_code": "12345",
                "country": "Test Country"
            },
            "payment_method": "credit_card",
            "notes": "Test order"
        }
        
        result = self.test_endpoint(
            "Create Order",
            "POST",
            "/orders/create/",
            order_data,
            201
        )
        
        if result:
            self.test_order_id = result.get("id")
            self.log(f"Order created with ID: {self.test_order_id}")
        
        # 2. List orders
        self.test_endpoint(
            "List Orders",
            "GET",
            "/orders/",
            expected_status=200
        )
        
        # 3. Get order detail
        if self.test_order_id:
            self.test_endpoint(
                "Get Order Detail",
                "GET",
                f"/orders/{self.test_order_id}/",
                expected_status=200
            )
            
            # 4. Update order
            update_data = {
                "status": "confirmed",
                "shipping_address": order_data["shipping_address"],
                "notes": "Updated test order"
            }
            
            self.test_endpoint(
                "Update Order",
                "PUT",
                f"/orders/{self.test_order_id}/",
                update_data,
                200
            )
    
    def test_documentation(self):
        """Test API documentation endpoints"""
        self.log("📚 Testing Documentation Endpoints", "HEADER")
        
        # 1. Test API schema
        self.test_endpoint(
            "API Schema",
            "GET",
            "/schema/",
            expected_status=200,
            auth_required=False
        )
        
        # 2. Test Swagger UI
        response = requests.get(f"{self.api_url}/docs/")
        if response.status_code == 200:
            self.log("✅ Swagger UI - Accessible", "SUCCESS")
        else:
            self.log(f"❌ Swagger UI - Status: {response.status_code}", "ERROR")
        
        # 3. Test ReDoc
        response = requests.get(f"{self.api_url}/redoc/")
        if response.status_code == 200:
            self.log("✅ ReDoc UI - Accessible", "SUCCESS")
        else:
            self.log(f"❌ ReDoc UI - Status: {response.status_code}", "ERROR")
    
    def cleanup(self):
        """Clean up test data"""
        self.log("🧹 Cleaning up test data", "HEADER")
        
        # Delete order (if created)
        if self.test_order_id:
            # Note: In a real app, you might not want to allow order deletion
            pass
        
        # Clear cart
        self.test_endpoint(
            "Final Cart Clear",
            "DELETE",
            "/cart/clear/",
            expected_status=204
        )
        
        # Delete product
        if self.test_product_slug:
            self.test_endpoint(
                "Delete Product",
                "DELETE",
                f"/products/{self.test_product_slug}/",
                expected_status=204
            )
        
        # Delete category
        if self.test_category_slug:
            self.test_endpoint(
                "Delete Category",
                "DELETE",
                f"/products/categories/{self.test_category_slug}/",
                expected_status=204
            )
        
        # Logout
        if self.refresh_token:
            logout_data = {"refresh": self.refresh_token}
            self.test_endpoint(
                "User Logout",
                "POST",
                "/auth/logout/",
                logout_data,
                200
            )
    
    def run_all_tests(self):
        """Run all API tests"""
        print("=" * 60)
        print("🚀 ALX Project Nexus API Comprehensive Testing")
        print("=" * 60)
        
        start_time = time.time()
        
        try:
            # Test server connectivity
            response = requests.get(self.base_url)
            if response.status_code != 200:
                self.log("❌ Server not accessible", "ERROR")
                return
            self.log("✅ Server is accessible", "SUCCESS")
            
            # Run test suites
            self.test_documentation()
            self.test_authentication()
            self.test_categories()
            self.test_products()
            self.test_cart()
            self.test_orders()
            
        except KeyboardInterrupt:
            self.log("Testing interrupted by user", "WARNING")
        except Exception as e:
            self.log(f"Unexpected error: {e}", "ERROR")
        finally:
            # Always try to cleanup
            try:
                self.cleanup()
            except:
                pass
        
        # Summary
        end_time = time.time()
        duration = end_time - start_time
        
        success_count = len([r for r in self.results if r["status"] == "SUCCESS"])
        error_count = len([r for r in self.results if r["status"] == "ERROR"])
        
        print("\n" + "=" * 60)
        print("📊 Test Summary")
        print("=" * 60)
        print(f"Duration: {duration:.2f} seconds")
        print(f"✅ Successful tests: {success_count}")
        print(f"❌ Failed tests: {error_count}")
        
        if error_count == 0:
            print("🎉 All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the logs above.")
        
        return error_count == 0

if __name__ == "__main__":
    # Allow custom base URL
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    
    tester = APITester(base_url)
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)
