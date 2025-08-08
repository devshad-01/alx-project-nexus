# 🗄️ Database Quick Reference - ALX E-Commerce Backend

## 🚀 Quick Setup Commands

```bash
# 1. Setup database (PostgreSQL)
./scripts/setup_database.sh

# 2. Validate setup
./scripts/validate_database.sh

# 3. Connect to database
psql -h localhost -U ecommerce_user -d ecommerce_backend
```

## 📊 Database Connection Details

| Parameter    | Value               |
| ------------ | ------------------- |
| **Database** | `alx_project` |
| **User**     | `shad`    |
| **Password** | `Qwerty.25`    |
| **Host**     | `localhost`         |
| **Port**     | `5432`              |

## 🎨 Visual ERD Creation

1. **Open**: https://dbdiagram.io/d
2. **Copy**: All content from `docs/database/dbdiagram_erd.txt`
3. **Paste**: Into dbdiagram.io editor
4. **Export**: Save as PNG/PDF for ALX submission

## 📋 Database Tables Overview

| Table            | Records      | Purpose                     |
| ---------------- | ------------ | --------------------------- |
| `users`          | 10+          | Customer and admin accounts |
| `categories`     | 8            | Product categorization      |
| `products`       | 22           | Core product catalog        |
| `product_images` | 44+          | Product image management    |
| `carts`          | Auto-created | User shopping carts         |
| `cart_items`     | Dynamic      | Items in shopping carts     |
| `orders`         | Sample data  | Customer orders             |
| `order_items`    | Sample data  | Order line items            |
| `reviews`        | Sample data  | Product reviews and ratings |

## 🔍 Useful Sample Queries

### **Product Catalog Queries**

```sql
-- All products with categories
SELECT p.name, p.price, c.name as category
FROM products p
JOIN categories c ON p.category_id = c.id
WHERE p.is_active = true;

-- Products by category
SELECT * FROM products
WHERE category_id = (SELECT id FROM categories WHERE name = 'Electronics');

-- Product search (full-text)
SELECT * FROM products
WHERE to_tsvector(name || ' ' || description) @@ plainto_tsquery('laptop');
```

### **Order and Cart Queries**

```sql
-- User order history
SELECT u.email, COUNT(o.id) as order_count, SUM(o.total_amount) as total_spent
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id, u.email;

-- Cart contents
SELECT u.email, p.name, ci.quantity, p.price, (ci.quantity * p.price) as total
FROM cart_items ci
JOIN carts c ON ci.cart_id = c.id
JOIN users u ON c.user_id = u.id
JOIN products p ON ci.product_id = p.id;
```

### **Analytics Queries**

```sql
-- Product popularity
SELECT p.name, COUNT(oi.id) as times_ordered, SUM(oi.quantity) as total_sold
FROM products p
LEFT JOIN order_items oi ON p.id = oi.product_id
GROUP BY p.id, p.name
ORDER BY times_ordered DESC;

-- Category performance
SELECT c.name, COUNT(p.id) as product_count, AVG(p.price) as avg_price
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
WHERE p.is_active = true
GROUP BY c.id, c.name;

-- Review statistics
SELECT p.name, COUNT(r.id) as review_count, ROUND(AVG(r.rating), 2) as avg_rating
FROM products p
LEFT JOIN reviews r ON p.id = r.product_id AND r.is_approved = true
GROUP BY p.id, p.name
HAVING COUNT(r.id) > 0;
```

## 🛠️ Admin Operations

### **Database Maintenance**

```sql
-- Refresh materialized view
REFRESH MATERIALIZED VIEW popular_products;

-- Generate new order number
SELECT generate_order_number();

-- Clean old cart items (older than 30 days)
SELECT cleanup_old_cart_items();
```

### **Data Validation**

```sql
-- Check data integrity
SELECT 'users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'categories', COUNT(*) FROM categories;

-- Verify foreign keys
SELECT COUNT(*) as orphaned_products
FROM products p
LEFT JOIN categories c ON p.category_id = c.id
WHERE c.id IS NULL;
```

## 🔧 Troubleshooting

### **Common Issues**

| Issue                      | Solution                               |
| -------------------------- | -------------------------------------- |
| Cannot connect to database | Run `sudo systemctl start postgresql`  |
| Permission denied          | Check user privileges with `GRANT ALL` |
| Table doesn't exist        | Re-run `setup_database.sh`             |
| No data in tables          | Re-run with seed data loading          |

### **Reset Database**

```bash
# Complete reset (destroys all data)
sudo -u postgres psql -c "DROP DATABASE IF EXISTS ecommerce_backend;"
sudo -u postgres psql -c "DROP USER IF EXISTS ecommerce_user;"
./scripts/setup_database.sh
```

## 📁 File Locations

| Component     | File Path                             |
| ------------- | ------------------------------------- |
| ERD Code      | `docs/database/dbdiagram_erd.txt`     |
| Schema        | `docs/database/postgresql_schema.sql` |
| Seed Data     | `docs/database/seed_data.sql`         |
| Django Models | `docs/database/django_models.py`      |
| Setup Script  | `scripts/setup_database.sh`           |
| Validation    | `scripts/validate_database.sh`        |

## 🎯 Next Steps

1. ✅ **Database Ready** - All components consistent and tested
2. 🎨 **Create ERD** - Use dbdiagram.io for visual representation
3. 🏗️ **Start Django** - Run setup and begin API development
4. 📝 **ALX Submission** - Export ERD and document your progress

**Status**: 🚀 **READY FOR DEVELOPMENT!**
