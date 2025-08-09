# API Documentation - E-Commerce Backend

## 📋 Overview

This document provides comprehensive documentation for the E-Commerce Backend API. The API follows RESTful conventions and provides endpoints for user management, product catalog, and order processing.

**Base URL**: `http://localhost:8000/api/`  
**API Version**: v1  
**Authentication**: JWT Bearer Token  

## 🔐 Authentication

### Authentication Flow

1. **Register**: Create a new user account
2. **Login**: Obtain JWT access and refresh tokens
3. **Access Protected Endpoints**: Include access token in Authorization header
4. **Refresh Token**: Use refresh token to get new access token when expired

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
}
```

**Response (201 Created)**:
```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com",
            "first_name": "John",
            "last_name": "Doe"
        },
        "tokens": {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
    },
    "message": "User registered successfully"
}
```

#### Login User
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

**Response (200 OK)**:
```json
{
    "success": true,
    "data": {
        "user": {
            "id": 1,
            "username": "johndoe",
            "email": "john@example.com"
        },
        "tokens": {
            "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
            "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
        }
    },
    "message": "Login successful"
}
```

#### Refresh Token
```http
POST /api/auth/refresh/
Content-Type: application/json

{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200 OK)**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## 📦 Products API

### Product Model
```json
{
    "id": "integer",
    "name": "string",
    "description": "string",
    "price": "decimal",
    "category": "object",
    "stock_quantity": "integer",
    "image": "string (URL)",
    "is_active": "boolean",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Product Endpoints

#### List Products
```http
GET /api/products/
```

**Query Parameters**:
- `category` (integer): Filter by category ID
- `min_price` (decimal): Minimum price filter
- `max_price` (decimal): Maximum price filter
- `search` (string): Search in product name and description
- `ordering` (string): Sort by field (price, -price, name, -name, created_at, -created_at)
- `page` (integer): Page number for pagination
- `page_size` (integer): Items per page (default: 20, max: 100)

**Example Request**:
```http
GET /api/products/?category=1&min_price=10&max_price=100&ordering=-price&page=1
```

**Response (200 OK)**:
```json
{
    "success": true,
    "data": {
        "count": 150,
        "next": "http://localhost:8000/api/products/?page=2",
        "previous": null,
        "results": [
            {
                "id": 1,
                "name": "Laptop Pro",
                "description": "High-performance laptop for professionals",
                "price": "999.99",
                "category": {
                    "id": 1,
                    "name": "Electronics",
                    "slug": "electronics"
                },
                "stock_quantity": 25,
                "image": "http://localhost:8000/media/products/laptop.jpg",
                "is_active": true,
                "created_at": "2025-08-09T10:00:00Z",
                "updated_at": "2025-08-09T10:00:00Z"
            }
        ]
    },
    "message": "Products retrieved successfully"
}
```

#### Get Product Details
```http
GET /api/products/{id}/
```

**Response (200 OK)**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "name": "Laptop Pro",
        "description": "High-performance laptop for professionals",
        "price": "999.99",
        "category": {
            "id": 1,
            "name": "Electronics",
            "slug": "electronics"
        },
        "stock_quantity": 25,
        "image": "http://localhost:8000/media/products/laptop.jpg",
        "is_active": true,
        "created_at": "2025-08-09T10:00:00Z",
        "updated_at": "2025-08-09T10:00:00Z"
    },
    "message": "Product retrieved successfully"
}
```

#### Create Product (Admin Only)
```http
POST /api/products/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "price": "decimal",
    "category": "integer",
    "stock_quantity": "integer",
    "image": "file (optional)"
}
```

#### Update Product (Admin Only)
```http
PUT /api/products/{id}/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "name": "string",
    "description": "string",
    "price": "decimal",
    "category": "integer",
    "stock_quantity": "integer"
}
```

#### Delete Product (Admin Only)
```http
DELETE /api/products/{id}/
Authorization: Bearer {access_token}
```

## 🏷 Categories API

### Category Model
```json
{
    "id": "integer",
    "name": "string",
    "slug": "string",
    "description": "string",
    "image": "string (URL)",
    "is_active": "boolean",
    "product_count": "integer"
}
```

### Category Endpoints

#### List Categories
```http
GET /api/categories/
```

**Response (200 OK)**:
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "name": "Electronics",
            "slug": "electronics",
            "description": "Electronic devices and gadgets",
            "image": "http://localhost:8000/media/categories/electronics.jpg",
            "is_active": true,
            "product_count": 45
        }
    ],
    "message": "Categories retrieved successfully"
}
```

## 🛒 Orders API

### Order Model
```json
{
    "id": "integer",
    "user": "object",
    "status": "string",
    "total_amount": "decimal",
    "items": "array",
    "shipping_address": "object",
    "created_at": "datetime",
    "updated_at": "datetime"
}
```

### Order Status Values
- `pending`: Order created, awaiting payment
- `confirmed`: Payment confirmed, processing
- `shipped`: Order shipped to customer
- `delivered`: Order delivered successfully
- `cancelled`: Order cancelled

### Order Endpoints

#### List User Orders
```http
GET /api/orders/
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
    "success": true,
    "data": {
        "count": 5,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 1,
                "status": "confirmed",
                "total_amount": "1299.98",
                "items_count": 2,
                "created_at": "2025-08-09T15:30:00Z"
            }
        ]
    },
    "message": "Orders retrieved successfully"
}
```

#### Get Order Details
```http
GET /api/orders/{id}/
Authorization: Bearer {access_token}
```

**Response (200 OK)**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "status": "confirmed",
        "total_amount": "1299.98",
        "items": [
            {
                "id": 1,
                "product": {
                    "id": 1,
                    "name": "Laptop Pro",
                    "price": "999.99"
                },
                "quantity": 1,
                "price": "999.99",
                "subtotal": "999.99"
            }
        ],
        "shipping_address": {
            "street": "123 Main St",
            "city": "New York",
            "state": "NY",
            "zip_code": "10001",
            "country": "USA"
        },
        "created_at": "2025-08-09T15:30:00Z",
        "updated_at": "2025-08-09T15:30:00Z"
    },
    "message": "Order retrieved successfully"
}
```

#### Create Order
```http
POST /api/orders/
Authorization: Bearer {access_token}
Content-Type: application/json

{
    "items": [
        {
            "product": 1,
            "quantity": 2
        }
    ],
    "shipping_address": {
        "street": "string",
        "city": "string",
        "state": "string",
        "zip_code": "string",
        "country": "string"
    }
}
```

**Response (201 Created)**:
```json
{
    "success": true,
    "data": {
        "id": 1,
        "status": "pending",
        "total_amount": "1999.98",
        "items": [...],
        "shipping_address": {...},
        "created_at": "2025-08-09T15:30:00Z"
    },
    "message": "Order created successfully"
}
```

## 📊 Response Format Standards

### Success Response Format
```json
{
    "success": true,
    "data": {
        // Response data object or array
    },
    "message": "Operation completed successfully"
}
```

### Error Response Format
```json
{
    "success": false,
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": {
            // Field-specific errors for validation
            "field_name": ["Error message for this field"]
        }
    }
}
```

## 🚫 Error Codes

### Authentication Errors (401)
- `AUTHENTICATION_REQUIRED`: Missing or invalid authentication
- `TOKEN_EXPIRED`: JWT token has expired
- `INVALID_CREDENTIALS`: Invalid username/password

### Authorization Errors (403)
- `PERMISSION_DENIED`: User lacks required permissions
- `ADMIN_REQUIRED`: Endpoint requires admin privileges

### Validation Errors (400)
- `VALIDATION_ERROR`: Request data validation failed
- `MISSING_REQUIRED_FIELD`: Required field not provided
- `INVALID_FORMAT`: Field format is incorrect

### Resource Errors (404)
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `USER_NOT_FOUND`: User account not found
- `PRODUCT_NOT_FOUND`: Product not found

### Server Errors (500)
- `INTERNAL_SERVER_ERROR`: Unexpected server error
- `DATABASE_ERROR`: Database operation failed

## 📝 Usage Examples

### Complete Workflow Example

1. **Register and Login**:
```bash
# Register new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "email": "demo@example.com", "password": "secure123"}'

# Login to get tokens
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "demo", "password": "secure123"}'
```

2. **Browse Products**:
```bash
# Get all categories
curl http://localhost:8000/api/categories/

# Browse electronics products
curl http://localhost:8000/api/products/?category=1&ordering=-price
```

3. **Place Order**:
```bash
# Create order with authentication
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [{"product": 1, "quantity": 1}],
    "shipping_address": {
      "street": "123 Main St",
      "city": "New York",
      "state": "NY",
      "zip_code": "10001",
      "country": "USA"
    }
  }'
```

## 🔧 Rate Limiting

API endpoints are rate-limited to ensure fair usage:

- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Admin users**: 5000 requests per hour

Rate limit headers are included in responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1692454800
```

## 📊 Pagination

List endpoints support pagination with the following parameters:

- `page`: Page number (default: 1)
- `page_size`: Items per page (default: 20, max: 100)

Pagination response includes:
```json
{
    "count": 150,
    "next": "http://localhost:8000/api/products/?page=3",
    "previous": "http://localhost:8000/api/products/?page=1",
    "results": [...]
}
```

---

**Interactive Documentation**: Visit `http://localhost:8000/api/docs/` for interactive Swagger UI documentation.

**API Schema**: Download the complete API schema at `http://localhost:8000/api/schema/`
