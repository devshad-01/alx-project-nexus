# E-Commerce Backend ERD Design

## 🎯 Database Design - Entity Relationship Diagram

**Project**: E-Commerce Backend - Project Nexus  
**Designer**: [Your Name]  
**Date**: August 7, 2025  
**Purpose**: Complete database schema design for e-commerce backend system

## 📊 Visual ERD Design

### 🎨 Interactive ERD Creation:

1. **Go to**: https://dbdiagram.io/d
2. **Copy content from**: `docs/database/dbdiagram_erd.txt`
3. **Paste into editor** for instant visual ERD
4. **Export**: Save as PNG/PDF for documentation

### 📁 ERD Source Files:

- **dbdiagram.io Code**: `docs/database/dbdiagram_erd.txt`
- **Database Schema**: `docs/database/postgresql_schema.sql`
- **Django Models**: `docs/database/django_models.py`

---

## 🗄️ Entity Specifications

### 1. User Entity

**Purpose**: Customer and admin user management with email authentication

| Field       | Type         | Constraints                 | Description                     |
| ----------- | ------------ | --------------------------- | ------------------------------- |
| id          | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Unique user identifier          |
| email       | VARCHAR(255) | UNIQUE, NOT NULL            | User's email (login credential) |
| password    | VARCHAR(128) | NOT NULL                    | Hashed password                 |
| first_name  | VARCHAR(150) |                             | User's first name               |
| last_name   | VARCHAR(150) |                             | User's last name                |
| is_staff    | BOOLEAN      | DEFAULT FALSE               | Admin privilege flag            |
| is_active   | BOOLEAN      | DEFAULT TRUE                | Account status                  |
| date_joined | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP   | Account creation date           |
| last_login  | TIMESTAMP    |                             | Last login timestamp            |

**Indexes**: email, is_active  
**Relationships**: One-to-One with Cart, One-to-Many with Orders, Reviews

### 2. Category Entity

**Purpose**: Product categorization and organization

| Field       | Type         | Constraints                         | Description                |
| ----------- | ------------ | ----------------------------------- | -------------------------- |
| id          | INTEGER      | PRIMARY KEY, AUTO_INCREMENT         | Unique category identifier |
| name        | VARCHAR(255) | UNIQUE, NOT NULL                    | Category name              |
| slug        | VARCHAR(255) | UNIQUE, NOT NULL                    | URL-friendly identifier    |
| description | TEXT         |                                     | Category description       |
| is_active   | BOOLEAN      | DEFAULT TRUE                        | Category status            |
| created_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP           | Creation timestamp         |
| updated_at  | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last update timestamp      |

**Indexes**: slug, is_active, name  
**Relationships**: One-to-Many with Products

### 3. Product Entity

**Purpose**: Core product information and inventory management

| Field          | Type          | Constraints                            | Description               |
| -------------- | ------------- | -------------------------------------- | ------------------------- |
| id             | INTEGER       | PRIMARY KEY, AUTO_INCREMENT            | Unique product identifier |
| name           | VARCHAR(255)  | NOT NULL                               | Product name              |
| slug           | VARCHAR(255)  | UNIQUE, NOT NULL                       | URL-friendly identifier   |
| description    | TEXT          |                                        | Product description       |
| price          | DECIMAL(10,2) | NOT NULL, CHECK (price > 0)            | Product price             |
| category_id    | INTEGER       | FOREIGN KEY (Category.id)              | Product category          |
| sku            | VARCHAR(100)  | UNIQUE, NOT NULL                       | Stock keeping unit        |
| stock_quantity | INTEGER       | DEFAULT 0, CHECK (stock_quantity >= 0) | Available inventory       |
| is_active      | BOOLEAN       | DEFAULT TRUE                           | Product availability      |
| is_featured    | BOOLEAN       | DEFAULT FALSE                          | Featured product flag     |
| created_by     | INTEGER       | FOREIGN KEY (User.id)                  | Product creator           |
| created_at     | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP              | Creation timestamp        |
| updated_at     | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP ON UPDATE    | Last update timestamp     |

**Indexes**: name, category_id, sku, is_active, price, created_at, (name, category_id)  
**Relationships**: Many-to-One with Category, One-to-Many with CartItems, OrderItems, Reviews

### 4. ProductImage Entity

**Purpose**: Product image management and display

| Field      | Type         | Constraints                 | Description                      |
| ---------- | ------------ | --------------------------- | -------------------------------- |
| id         | INTEGER      | PRIMARY KEY, AUTO_INCREMENT | Unique image identifier          |
| product_id | INTEGER      | FOREIGN KEY (Product.id)    | Associated product               |
| image_url  | VARCHAR(500) | NOT NULL                    | Image file path/URL              |
| alt_text   | VARCHAR(255) |                             | Image alt text for accessibility |
| is_primary | BOOLEAN      | DEFAULT FALSE               | Primary product image flag       |
| sort_order | INTEGER      | DEFAULT 0                   | Display order                    |
| created_at | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP   | Upload timestamp                 |

**Indexes**: product_id, is_primary  
**Relationships**: Many-to-One with Product

### 5. Cart Entity

**Purpose**: User shopping cart management

| Field      | Type      | Constraints                         | Description            |
| ---------- | --------- | ----------------------------------- | ---------------------- |
| id         | INTEGER   | PRIMARY KEY, AUTO_INCREMENT         | Unique cart identifier |
| user_id    | INTEGER   | FOREIGN KEY (User.id), UNIQUE       | Cart owner             |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP           | Cart creation date     |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last modification      |

**Indexes**: user_id  
**Relationships**: One-to-One with User, One-to-Many with CartItems

### 6. CartItem Entity

**Purpose**: Individual items within shopping carts

| Field      | Type      | Constraints                         | Description                 |
| ---------- | --------- | ----------------------------------- | --------------------------- |
| id         | INTEGER   | PRIMARY KEY, AUTO_INCREMENT         | Unique cart item identifier |
| cart_id    | INTEGER   | FOREIGN KEY (Cart.id)               | Associated cart             |
| product_id | INTEGER   | FOREIGN KEY (Product.id)            | Product in cart             |
| quantity   | INTEGER   | NOT NULL, CHECK (quantity > 0)      | Item quantity               |
| added_at   | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP           | Item add timestamp          |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last quantity update        |

**Indexes**: cart_id, product_id, (cart_id, product_id)  
**Constraints**: UNIQUE(cart_id, product_id)  
**Relationships**: Many-to-One with Cart and Product

### 7. Order Entity

**Purpose**: Customer order management and tracking

| Field            | Type          | Constraints                         | Description             |
| ---------------- | ------------- | ----------------------------------- | ----------------------- |
| id               | INTEGER       | PRIMARY KEY, AUTO_INCREMENT         | Unique order identifier |
| order_number     | VARCHAR(50)   | UNIQUE, NOT NULL                    | Human-readable order ID |
| user_id          | INTEGER       | FOREIGN KEY (User.id)               | Order customer          |
| total_amount     | DECIMAL(10,2) | NOT NULL, CHECK (total_amount > 0)  | Order total value       |
| status           | VARCHAR(20)   | DEFAULT 'pending'                   | Order status            |
| shipping_address | JSON          | NOT NULL                            | Delivery address        |
| billing_address  | JSON          |                                     | Billing address         |
| payment_method   | VARCHAR(50)   |                                     | Payment method used     |
| notes            | TEXT          |                                     | Order notes             |
| created_at       | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP           | Order creation date     |
| updated_at       | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP ON UPDATE | Last status update      |

**Status Values**: 'pending', 'confirmed', 'processing', 'shipped', 'delivered', 'cancelled'  
**Indexes**: user_id, status, order_number, created_at  
**Relationships**: Many-to-One with User, One-to-Many with OrderItems

### 8. OrderItem Entity

**Purpose**: Individual products within orders

| Field       | Type          | Constraints                       | Description                  |
| ----------- | ------------- | --------------------------------- | ---------------------------- |
| id          | INTEGER       | PRIMARY KEY, AUTO_INCREMENT       | Unique order item identifier |
| order_id    | INTEGER       | FOREIGN KEY (Order.id)            | Associated order             |
| product_id  | INTEGER       | FOREIGN KEY (Product.id)          | Ordered product              |
| quantity    | INTEGER       | NOT NULL, CHECK (quantity > 0)    | Ordered quantity             |
| unit_price  | DECIMAL(10,2) | NOT NULL, CHECK (unit_price > 0)  | Price per unit at order time |
| total_price | DECIMAL(10,2) | NOT NULL, CHECK (total_price > 0) | Total item price             |
| created_at  | TIMESTAMP     | DEFAULT CURRENT_TIMESTAMP         | Item creation timestamp      |

**Indexes**: order_id, product_id  
**Relationships**: Many-to-One with Order and Product

### 9. Review Entity

**Purpose**: Product reviews and ratings from customers

| Field         | Type         | Constraints                                   | Description              |
| ------------- | ------------ | --------------------------------------------- | ------------------------ |
| id            | INTEGER      | PRIMARY KEY, AUTO_INCREMENT                   | Unique review identifier |
| user_id       | INTEGER      | FOREIGN KEY (User.id)                         | Review author            |
| product_id    | INTEGER      | FOREIGN KEY (Product.id)                      | Reviewed product         |
| rating        | INTEGER      | NOT NULL, CHECK (rating >= 1 AND rating <= 5) | Star rating (1-5)        |
| title         | VARCHAR(255) |                                               | Review title             |
| comment       | TEXT         |                                               | Review comment           |
| is_verified   | BOOLEAN      | DEFAULT FALSE                                 | Verified purchase flag   |
| is_approved   | BOOLEAN      | DEFAULT TRUE                                  | Review approval status   |
| helpful_count | INTEGER      | DEFAULT 0                                     | Helpful votes count      |
| created_at    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP                     | Review creation date     |
| updated_at    | TIMESTAMP    | DEFAULT CURRENT_TIMESTAMP ON UPDATE           | Last edit timestamp      |

**Indexes**: product_id, user_id, rating, is_approved  
**Constraints**: UNIQUE(user_id, product_id)  
**Relationships**: Many-to-One with User and Product

---

## 🔗 Relationship Summary

### Primary Relationships:

```
User (1) ←→ (1) Cart
User (1) ←→ (N) Orders
User (1) ←→ (N) Reviews

Category (1) ←→ (N) Products
Product (1) ←→ (N) ProductImages
Product (1) ←→ (N) CartItems
Product (1) ←→ (N) OrderItems
Product (1) ←→ (N) Reviews

Cart (1) ←→ (N) CartItems
Order (1) ←→ (N) OrderItems
```

### Business Rules:

1. **One Cart per User**: Each user has exactly one persistent cart
2. **Unique Cart Items**: One product can appear only once per cart (update quantity instead)
3. **One Review per Product per User**: Users can review each product only once
4. **Order Immutability**: Order items preserve price at time of purchase
5. **Stock Management**: Product stock decreases when orders are confirmed
6. **Soft Deletion**: Products and categories use `is_active` for soft deletion

---

## 🔧 Database Optimization Strategy

### Primary Indexes (Auto-created):

- All primary keys (id fields)
- Unique constraints (email, sku, order_number, etc.)

### Performance Indexes:

```sql
-- User queries
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);

-- Product searches and filtering
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_featured ON products(is_featured);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_name_category ON products(name, category_id);

-- Order queries
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_date ON orders(created_at);

-- Review aggregations
CREATE INDEX idx_reviews_product_rating ON reviews(product_id, rating);
CREATE INDEX idx_reviews_approved ON reviews(is_approved);
```

### Full-Text Search:

```sql
-- PostgreSQL full-text search for products
CREATE INDEX idx_products_search ON products USING gin(to_tsvector('english', name || ' ' || description));
```

---

## ✅ ERD Validation Checklist

- [ ] **Entity Completeness**: All business entities identified
- [ ] **Relationship Accuracy**: All relationships properly defined
- [ ] **Normalization**: Database is in 3rd Normal Form (3NF)
- [ ] **Constraint Definition**: All business rules enforced at database level
- [ ] **Index Strategy**: Performance indexes planned for common queries
- [ ] **Scalability**: Design supports future growth
- [ ] **Data Integrity**: Foreign key constraints properly defined
- [ ] **Security**: Sensitive data properly handled

---

## 📋 Next Steps

1. **Create ERD Visually**: Use Lucidchart or Draw.io to create the visual diagram
2. **Export to Google Doc**: Make it publicly accessible for submission
3. **Validate with Team**: Review the design before implementation
4. **Begin Django Models**: Implement models based on this ERD design
5. **Generate Migrations**: Use Django commands to create database schema

---

**Remember**: This ERD serves as the blueprint for your entire database implementation. Any changes to this design should be documented and reflected in the visual ERD before making code changes.
