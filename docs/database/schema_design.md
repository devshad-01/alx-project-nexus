# Database Schema Design - E-Commerce Backend

## Entity Relationship Diagram (ERD)

### Core Entities Overview

The e-commerce database is designed with the following core entities and their relationships:

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│    User     │       │  Category   │       │   Product   │
│─────────────│       │─────────────│       │─────────────│
│ id (PK)     │       │ id (PK)     │       │ id (PK)     │
│ email       │       │ name        │       │ name        │
│ password    │       │ description │   ┌───│ category_id │
│ first_name  │       │ slug        │   │   │ price       │
│ last_name   │       │ is_active   │   │   │ description │
│ is_staff    │       │ created_at  │   │   │ sku         │
│ is_active   │       │ updated_at  │   │   │ stock_qty   │
│ date_joined │       └─────────────┘   │   │ is_active   │
│ last_login  │                         │   │ created_by  │
└─────────────┘                         │   │ created_at  │
       │                                │   │ updated_at  │
       │                                │   └─────────────┘
       │                                │
       │    ┌─────────────┐             │
       │    │    Cart     │             │
       │    │─────────────│             │
       └────│ user_id     │             │
            │ created_at  │             │
            │ updated_at  │             │
            └─────────────┘             │
                   │                    │
                   │                    │
            ┌─────────────┐             │
            │  CartItem   │             │
            │─────────────│             │
            │ id (PK)     │             │
        ┌───│ cart_id     │             │
        │   │ product_id  │─────────────┘
        │   │ quantity    │
        │   │ created_at  │
        │   │ updated_at  │
        │   └─────────────┘
        │
        │   ┌─────────────┐
        │   │    Order    │
        │   │─────────────│
        │   │ id (PK)     │
        └───│ user_id     │
            │ order_number│
            │ total_amount│
            │ status      │
            │ ship_address│
            │ created_at  │
            │ updated_at  │
            └─────────────┘
                   │
                   │
            ┌─────────────┐
            │  OrderItem  │
            │─────────────│
            │ id (PK)     │
        ┌───│ order_id    │
        │   │ product_id  │─────────────┐
        │   │ quantity    │             │
        │   │ price       │             │
        │   │ created_at  │             │
        │   └─────────────┘             │
        │                               │
        │   ┌─────────────┐             │
        │   │   Review    │             │
        │   │─────────────│             │
        │   │ id (PK)     │             │
        └───│ user_id     │             │
            │ product_id  │─────────────┘
            │ rating      │
            │ comment     │
            │ is_verified │
            │ created_at  │
            │ updated_at  │
            └─────────────┘
```

## Detailed Entity Specifications

### 1. User Model

**Purpose**: Custom user model for authentication and user management

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(150),
    last_name VARCHAR(150),
    is_staff BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT TRUE,
    date_joined TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_active ON users(is_active);
```

**Django Model**:

```python
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
```

### 2. Category Model

**Purpose**: Product categorization and organization

```sql
CREATE TABLE categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    slug VARCHAR(255) UNIQUE NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_categories_slug ON categories(slug);
CREATE INDEX idx_categories_active ON categories(is_active);
```

**Django Model**:

```python
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = "Categories"
```

### 3. Product Model

**Purpose**: Core product information and inventory management

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    category_id INTEGER REFERENCES categories(id),
    sku VARCHAR(100) UNIQUE NOT NULL,
    stock_quantity INTEGER DEFAULT 0,
    is_active BOOLEAN DEFAULT TRUE,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT positive_price CHECK (price > 0),
    CONSTRAINT non_negative_stock CHECK (stock_quantity >= 0)
);

-- Indexes for performance
CREATE INDEX idx_products_category ON products(category_id);
CREATE INDEX idx_products_sku ON products(sku);
CREATE INDEX idx_products_active ON products(is_active);
CREATE INDEX idx_products_name ON products(name);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_name_category ON products(name, category_id);
```

**Django Model**:

```python
class Product(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    sku = models.CharField(max_length=100, unique=True)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True, db_index=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_products'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['name', 'category']),
            models.Index(fields=['price']),
            models.Index(fields=['created_at']),
        ]
```

### 4. ProductImage Model

**Purpose**: Product image management

```sql
CREATE TABLE product_images (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    image VARCHAR(255) NOT NULL,
    alt_text VARCHAR(255),
    is_primary BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_product_images_product ON product_images(product_id);
CREATE INDEX idx_product_images_primary ON product_images(is_primary);
```

**Django Model**:

```python
class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='products/')
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

### 5. Cart Model

**Purpose**: Shopping cart management for users

```sql
CREATE TABLE carts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER UNIQUE REFERENCES users(id) ON DELETE CASCADE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes
CREATE INDEX idx_carts_user ON carts(user_id);
```

**Django Model**:

```python
class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='cart'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_amount(self):
        return sum(item.subtotal for item in self.items.all())

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())
```

### 6. CartItem Model

**Purpose**: Individual items within a shopping cart

```sql
CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    cart_id INTEGER REFERENCES carts(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id) ON DELETE CASCADE,
    quantity INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT positive_quantity CHECK (quantity > 0),
    CONSTRAINT unique_cart_product UNIQUE(cart_id, product_id)
);

-- Indexes
CREATE INDEX idx_cart_items_cart ON cart_items(cart_id);
CREATE INDEX idx_cart_items_product ON cart_items(product_id);
```

**Django Model**:

```python
class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['cart', 'product']

    @property
    def subtotal(self):
        return self.product.price * self.quantity
```

### 7. Order Model

**Purpose**: Order management and tracking

```sql
CREATE TABLE orders (
    id SERIAL PRIMARY KEY,
    order_number VARCHAR(50) UNIQUE NOT NULL,
    user_id INTEGER REFERENCES users(id),
    total_amount DECIMAL(10, 2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    shipping_address JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT positive_total CHECK (total_amount > 0)
);

-- Indexes
CREATE INDEX idx_orders_user ON orders(user_id);
CREATE INDEX idx_orders_status ON orders(status);
CREATE INDEX idx_orders_created ON orders(created_at);
CREATE INDEX idx_orders_number ON orders(order_number);
```

**Django Model**:

```python
class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        db_index=True
    )
    shipping_address = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
```

### 8. OrderItem Model

**Purpose**: Individual items within an order

```sql
CREATE TABLE order_items (
    id SERIAL PRIMARY KEY,
    order_id INTEGER REFERENCES orders(id) ON DELETE CASCADE,
    product_id INTEGER REFERENCES products(id),
    quantity INTEGER NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT positive_quantity CHECK (quantity > 0),
    CONSTRAINT positive_price CHECK (price > 0)
);

-- Indexes
CREATE INDEX idx_order_items_order ON order_items(order_id);
CREATE INDEX idx_order_items_product ON order_items(product_id);
```

**Django Model**:

```python
class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items'
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        return self.price * self.quantity
```

### 9. Review Model

**Purpose**: Product reviews and ratings

```sql
CREATE TABLE reviews (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    product_id INTEGER REFERENCES products(id),
    rating INTEGER NOT NULL,
    comment TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT rating_range CHECK (rating >= 1 AND rating <= 5),
    CONSTRAINT unique_user_product_review UNIQUE(user_id, product_id)
);

-- Indexes
CREATE INDEX idx_reviews_product ON reviews(product_id);
CREATE INDEX idx_reviews_user ON reviews(user_id);
CREATE INDEX idx_reviews_rating ON reviews(rating);
```

**Django Model**:

```python
class Review(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'product']
        ordering = ['-created_at']
```

## Database Optimization Strategies

### 1. Indexing Strategy

**Primary Indexes (automatically created):**

- Primary keys on all tables
- Unique constraints on email, sku, order_number, etc.

**Secondary Indexes for performance:**

```sql
-- Product search and filtering
CREATE INDEX idx_products_name_trgm ON products USING gin(name gin_trgm_ops);
CREATE INDEX idx_products_search ON products(name, category_id, is_active);

-- Order queries
CREATE INDEX idx_orders_user_status ON orders(user_id, status);
CREATE INDEX idx_orders_date_range ON orders(created_at DESC);

-- Review aggregations
CREATE INDEX idx_reviews_product_rating ON reviews(product_id, rating);
```

### 2. Query Optimization Techniques

**Use Django ORM efficiently:**

```python
# Good: Use select_related for foreign keys
products = Product.objects.select_related('category').filter(is_active=True)

# Good: Use prefetch_related for reverse foreign keys
products = Product.objects.prefetch_related('reviews', 'images')

# Good: Use annotations for aggregations
products = Product.objects.annotate(
    avg_rating=Avg('reviews__rating'),
    review_count=Count('reviews')
)

# Bad: N+1 query problem
for product in Product.objects.all():
    print(product.category.name)  # Separate query for each product
```

### 3. Database Constraints and Validation

**Data Integrity Constraints:**

```sql
-- Ensure positive values
ALTER TABLE products ADD CONSTRAINT positive_price CHECK (price > 0);
ALTER TABLE products ADD CONSTRAINT non_negative_stock CHECK (stock_quantity >= 0);

-- Ensure valid ratings
ALTER TABLE reviews ADD CONSTRAINT rating_range CHECK (rating >= 1 AND rating <= 5);

-- Prevent duplicate reviews
ALTER TABLE reviews ADD CONSTRAINT unique_user_product_review UNIQUE(user_id, product_id);

-- Prevent duplicate cart items
ALTER TABLE cart_items ADD CONSTRAINT unique_cart_product UNIQUE(cart_id, product_id);
```

### 4. Performance Monitoring Queries

**Identify slow queries:**

```sql
-- Enable query logging in PostgreSQL
ALTER SYSTEM SET log_statement = 'all';
ALTER SYSTEM SET log_min_duration_statement = 1000;  -- Log queries > 1 second

-- Find most expensive queries
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
```

**Monitor index usage:**

```sql
-- Check index usage statistics
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read, idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

## Scalability Considerations

### 1. Partitioning Strategy

**Order Partitioning by Date:**

```sql
-- Partition orders table by month
CREATE TABLE orders_2025_08 PARTITION OF orders
FOR VALUES FROM ('2025-08-01') TO ('2025-09-01');

CREATE TABLE orders_2025_09 PARTITION OF orders
FOR VALUES FROM ('2025-09-01') TO ('2025-10-01');
```

### 2. Read Replicas

**Configure read replicas for scaling reads:**

```python
# Django database routing
class DatabaseRouter:
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['products', 'reviews']:
            return 'read_replica'
        return 'default'

    def db_for_write(self, model, **hints):
        return 'default'
```

### 3. Caching Strategy

**Multi-level caching:**

```python
# Redis caching for expensive queries
from django.core.cache import cache

def get_featured_products():
    cache_key = 'featured_products_v1'
    products = cache.get(cache_key)

    if products is None:
        products = list(Product.objects.filter(
            is_featured=True,
            is_active=True
        ).select_related('category')[:20])
        cache.set(cache_key, products, 3600)  # 1 hour

    return products
```

This database design provides a solid foundation for the e-commerce backend with proper relationships, constraints, and optimization strategies for scalability and performance.
