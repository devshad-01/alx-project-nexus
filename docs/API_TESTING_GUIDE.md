# 🧪 ALX Project Nexus - API Testing Guide

**Server URL**: `http://localhost:8000`  
**Status**: ✅ Running  

## 🔐 **Authentication Flow Testing**

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Expected Response**: 
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "Test",
    "last_name": "User"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

### 2. User Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

### 3. Access Protected Endpoint
```bash
# Use the access token from registration/login
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## 📦 **Products API Testing**

### 1. List Products (Public)
```bash
curl -X GET http://localhost:8000/api/products/
```

### 2. Product Search
```bash
curl -X GET "http://localhost:8000/api/products/search/?q=laptop"
```

### 3. Filter Products
```bash
curl -X GET "http://localhost:8000/api/products/?category=electronics&min_price=100&max_price=1000"
```

### 4. Create Product (Admin Required)
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Gaming Laptop",
    "description": "High-performance gaming laptop",
    "price": "1299.99",
    "category": 1,
    "stock_quantity": 10,
    "sku": "LAPTOP001"
  }'
```

## 🛒 **Orders API Testing**

### 1. Create Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {
        "product": 1,
        "quantity": 2
      }
    ],
    "shipping_address": "123 Main St, City, State 12345"
  }'
```

### 2. List User Orders
```bash
curl -X GET http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 3. Track Order
```bash
curl -X GET http://localhost:8000/api/orders/track/ORD-20250809-001/
```

## 🛍️ **Shopping Cart Testing**

### 1. View Cart
```bash
curl -X GET http://localhost:8000/api/core/cart/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 2. Add to Cart
```bash
curl -X POST http://localhost:8000/api/core/cart/add/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 2
  }'
```

### 3. Update Cart Item
```bash
curl -X PUT http://localhost:8000/api/core/cart/update/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "product_id": 1,
    "quantity": 3
  }'
```

## 🔧 **Admin & Utility Endpoints**

### 1. API Documentation
```bash
# View Swagger documentation
curl -X GET http://localhost:8000/api/docs/
```

### 2. Admin Interface
- Visit: `http://localhost:8000/admin/`
- Login with superuser credentials
- Manage all models through web interface

### 3. Debug Toolbar (Development)
- Available when accessing endpoints via browser
- Shows SQL queries, performance metrics
- Visible in development mode only

## 📊 **API Response Formats**

### Success Response Structure
```json
{
  "message": "Operation successful",
  "data": { /* relevant data */ },
  "status": "success"
}
```

### Error Response Structure
```json
{
  "error": "Error description",
  "details": { /* error details */ },
  "status": "error"
}
```

### Pagination Response
```json
{
  "count": 100,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [ /* paginated data */ ]
}
```

## 🚀 **Quick Test Sequence**

For rapid demonstration to mentors:

```bash
# 1. Check server status
curl -X GET http://localhost:8000/api/docs/

# 2. Register test user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username":"demo","email":"demo@test.com","password":"pass123","password_confirm":"pass123","first_name":"Demo","last_name":"User"}'

# 3. Login and get token
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@test.com","password":"pass123"}'

# 4. Test protected endpoint (use token from step 3)
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer TOKEN_FROM_STEP_3"

# 5. View products
curl -X GET http://localhost:8000/api/products/

# 6. Search products
curl -X GET "http://localhost:8000/api/products/search/?q=test"
```

## 🎯 **Testing Checklist**

### ✅ **Authentication**
- [ ] User registration works
- [ ] User login returns JWT tokens
- [ ] Protected endpoints require authentication
- [ ] Token refresh mechanism works
- [ ] Profile management functional

### ✅ **Products**
- [ ] Product listing with pagination
- [ ] Product search functionality
- [ ] Product filtering by category/price
- [ ] CRUD operations (admin)
- [ ] Product images and reviews

### ✅ **Orders**
- [ ] Order creation process
- [ ] Order status tracking
- [ ] User order history
- [ ] Admin order management
- [ ] Inventory updates

### ✅ **General**
- [ ] Error handling works correctly
- [ ] API documentation accessible
- [ ] Admin interface functional
- [ ] CORS headers present
- [ ] Proper HTTP status codes

---

**STATUS**: 🟢 **ALL ENDPOINTS READY FOR TESTING**  
**NEXT STEP**: 🧪 **RUN TEST SEQUENCE WITH ACTUAL DATA**
