-- E-Commerce Backend Seed Data
-- ALX Project Nexus - Development and Testing Data
-- Generated: August 7, 2025

-- ==========================================
-- SEED DATA FOR DEVELOPMENT
-- ==========================================

-- Clear existing data (for development only)
-- TRUNCATE TABLE reviews, order_items, orders, cart_items, carts, product_images, products, categories, users RESTART IDENTITY CASCADE;

-- ==========================================
-- USERS SEED DATA
-- ==========================================
INSERT INTO users (email, password, first_name, last_name, is_staff, is_active) VALUES
-- Admin users (password: admin123)
('admin@ecommerce.com', 'pbkdf2_sha256$600000$abc123$abc123def456ghi789', 'Admin', 'User', TRUE, TRUE),
('manager@ecommerce.com', 'pbkdf2_sha256$600000$def456$def456ghi789jkl012', 'Store', 'Manager', TRUE, TRUE),

-- Customer users (password: user123)
('john.doe@email.com', 'pbkdf2_sha256$600000$ghi789$ghi789jkl012mno345', 'John', 'Doe', FALSE, TRUE),
('jane.smith@email.com', 'pbkdf2_sha256$600000$jkl012$jkl012mno345pqr678', 'Jane', 'Smith', FALSE, TRUE),
('mike.johnson@email.com', 'pbkdf2_sha256$600000$mno345$mno345pqr678stu901', 'Mike', 'Johnson', FALSE, TRUE),
('sarah.wilson@email.com', 'pbkdf2_sha256$600000$pqr678$pqr678stu901vwx234', 'Sarah', 'Wilson', FALSE, TRUE),
('david.brown@email.com', 'pbkdf2_sha256$600000$stu901$stu901vwx234yzab567', 'David', 'Brown', FALSE, TRUE),
('lisa.garcia@email.com', 'pbkdf2_sha256$600000$vwx234$vwx234yzab567cdef890', 'Lisa', 'Garcia', FALSE, TRUE),
('tom.anderson@email.com', 'pbkdf2_sha256$600000$yzab567$yzab567cdef890ghij123', 'Tom', 'Anderson', FALSE, TRUE),
('emma.taylor@email.com', 'pbkdf2_sha256$600000$cdef890$cdef890ghij123klmn456', 'Emma', 'Taylor', FALSE, TRUE);

-- ==========================================
-- CATEGORIES SEED DATA
-- ==========================================
INSERT INTO categories (name, slug, description, is_active) VALUES
('Electronics', 'electronics', 'Electronic devices and accessories', TRUE),
('Clothing', 'clothing', 'Fashion and apparel for all ages', TRUE),
('Books', 'books', 'Books across all genres and categories', TRUE),
('Home & Garden', 'home-garden', 'Home improvement and garden supplies', TRUE),
('Sports & Outdoors', 'sports-outdoors', 'Sports equipment and outdoor gear', TRUE),
('Beauty & Health', 'beauty-health', 'Beauty products and health supplements', TRUE),
('Toys & Games', 'toys-games', 'Toys, games, and entertainment', TRUE),
('Automotive', 'automotive', 'Car parts and automotive accessories', TRUE);

-- ==========================================
-- PRODUCTS SEED DATA
-- ==========================================
INSERT INTO products (name, slug, description, price, category_id, sku, stock_quantity, is_active, is_featured, created_by) VALUES

-- Electronics
('iPhone 15 Pro', 'iphone-15-pro', 'Latest iPhone with advanced camera system and A17 Pro chip', 999.99, 1, 'IPH15PRO001', 50, TRUE, TRUE, 1),
('Samsung Galaxy S24', 'samsung-galaxy-s24', 'Premium Android smartphone with AI features', 899.99, 1, 'SAM24GAL001', 45, TRUE, TRUE, 1),
('MacBook Air M3', 'macbook-air-m3', '13-inch laptop with M3 chip and all-day battery', 1199.99, 1, 'MBA13M3001', 30, TRUE, TRUE, 1),
('Sony WH-1000XM5', 'sony-wh-1000xm5', 'Industry-leading noise canceling headphones', 399.99, 1, 'SONYWH5001', 75, TRUE, FALSE, 1),
('iPad Pro 12.9"', 'ipad-pro-12-9', 'Professional tablet with M2 chip and Liquid Retina display', 1099.99, 1, 'IPADPRO129', 25, TRUE, TRUE, 1),

-- Clothing
('Levi''s 501 Jeans', 'levis-501-jeans', 'Classic straight-leg jeans in vintage blue', 69.99, 2, 'LEV501JEAN', 100, TRUE, FALSE, 1),
('Nike Air Force 1', 'nike-air-force-1', 'Iconic basketball shoes in white leather', 119.99, 2, 'NIKEAF1WHT', 80, TRUE, TRUE, 2),
('Adidas Hoodie', 'adidas-hoodie', 'Comfortable cotton blend hoodie with logo', 79.99, 2, 'ADIHOODIE01', 60, TRUE, FALSE, 2),
('Ray-Ban Sunglasses', 'rayban-sunglasses', 'Classic aviator sunglasses with UV protection', 159.99, 2, 'RAYBANAVI01', 40, TRUE, FALSE, 2),

-- Books
('The Psychology of Money', 'psychology-of-money', 'Timeless lessons on wealth and happiness', 19.99, 3, 'PSYMONEY001', 200, TRUE, TRUE, 1),
('Atomic Habits', 'atomic-habits', 'Tiny changes that create remarkable results', 18.99, 3, 'ATOMHAB001', 150, TRUE, TRUE, 1),
('Clean Code', 'clean-code', 'A handbook of agile software craftsmanship', 49.99, 3, 'CLEANCODE01', 75, TRUE, FALSE, 1),
('The Lean Startup', 'lean-startup', 'How today''s entrepreneurs use innovation', 24.99, 3, 'LEANSTART01', 90, TRUE, FALSE, 1),

-- Home & Garden
('Dyson V15 Vacuum', 'dyson-v15-vacuum', 'Cordless vacuum with laser dust detection', 749.99, 4, 'DYSONV15001', 20, TRUE, TRUE, 2),
('Instant Pot Duo', 'instant-pot-duo', '7-in-1 electric pressure cooker', 89.99, 4, 'INSTPOT7IN1', 65, TRUE, FALSE, 2),
('Philips Hue Lights', 'philips-hue-lights', 'Smart LED light bulbs with color changing', 199.99, 4, 'PHILHUE4PK', 35, TRUE, FALSE, 2),

-- Sports & Outdoors
('NordicTrack Treadmill', 'nordictrack-treadmill', 'Commercial-grade treadmill with iFit', 1299.99, 5, 'NORDTREAD01', 10, TRUE, TRUE, 2),
('Yeti Cooler 45', 'yeti-cooler-45', 'Rotomolded cooler that keeps ice for days', 349.99, 5, 'YETICOOL45', 25, TRUE, FALSE, 2),
('Patagonia Backpack', 'patagonia-backpack', '30L hiking backpack with laptop compartment', 129.99, 5, 'PATBACK30L', 40, TRUE, FALSE, 2),

-- Beauty & Health
('Olaplex Hair Treatment', 'olaplex-hair-treatment', 'Professional hair repair treatment', 28.99, 6, 'OLAPLEX001', 80, TRUE, FALSE, 2),
('Vitamin D3 Supplements', 'vitamin-d3-supplements', 'High-potency vitamin D3 for immune support', 24.99, 6, 'VITD3SUPP', 120, TRUE, FALSE, 2),

-- Toys & Games
('LEGO Architecture Set', 'lego-architecture-set', 'Famous landmark building set for adults', 199.99, 7, 'LEGOARCH01', 30, TRUE, TRUE, 1),
('Nintendo Switch OLED', 'nintendo-switch-oled', 'Gaming console with 7-inch OLED screen', 349.99, 7, 'NINTSWOL01', 45, TRUE, TRUE, 1),

-- Automotive
('Tesla Model Y Floor Mats', 'tesla-model-y-mats', 'All-weather floor mats for Tesla Model Y', 149.99, 8, 'TESMATYMAT', 50, TRUE, FALSE, 2),
('Car Phone Mount', 'car-phone-mount', 'Magnetic dashboard phone holder', 29.99, 8, 'CARPHOMNT1', 100, TRUE, FALSE, 2);

-- ==========================================
-- PRODUCT IMAGES SEED DATA
-- ==========================================
INSERT INTO product_images (product_id, image_url, alt_text, is_primary, sort_order) VALUES
-- iPhone 15 Pro images
(1, '/images/products/iphone-15-pro-main.jpg', 'iPhone 15 Pro front view', TRUE, 0),
(1, '/images/products/iphone-15-pro-back.jpg', 'iPhone 15 Pro back view', FALSE, 1),
(1, '/images/products/iphone-15-pro-colors.jpg', 'iPhone 15 Pro color options', FALSE, 2),

-- Samsung Galaxy S24 images
(2, '/images/products/samsung-s24-main.jpg', 'Samsung Galaxy S24 front view', TRUE, 0),
(2, '/images/products/samsung-s24-camera.jpg', 'Samsung Galaxy S24 camera system', FALSE, 1),

-- MacBook Air M3 images
(3, '/images/products/macbook-air-m3-main.jpg', 'MacBook Air M3 opened view', TRUE, 0),
(3, '/images/products/macbook-air-m3-ports.jpg', 'MacBook Air M3 ports detail', FALSE, 1),

-- Nike Air Force 1 images
(7, '/images/products/nike-af1-main.jpg', 'Nike Air Force 1 side view', TRUE, 0),
(7, '/images/products/nike-af1-detail.jpg', 'Nike Air Force 1 sole detail', FALSE, 1),

-- LEGO Architecture images
(19, '/images/products/lego-arch-main.jpg', 'LEGO Architecture completed model', TRUE, 0),
(19, '/images/products/lego-arch-box.jpg', 'LEGO Architecture packaging', FALSE, 1);

-- ==========================================
-- CARTS SEED DATA
-- ==========================================
INSERT INTO carts (user_id) VALUES
(3), (4), (5), (6), (7), (8), (9), (10);

-- ==========================================
-- CART ITEMS SEED DATA
-- ==========================================
INSERT INTO cart_items (cart_id, product_id, quantity) VALUES
-- John Doe's cart
(1, 1, 1),  -- iPhone 15 Pro
(1, 4, 1),  -- Sony headphones

-- Jane Smith's cart
(2, 7, 1),  -- Nike shoes
(2, 8, 1),  -- Adidas hoodie
(2, 10, 2), -- Books

-- Mike Johnson's cart
(3, 3, 1),  -- MacBook Air
(3, 5, 1),  -- iPad Pro

-- Sarah Wilson's cart
(4, 13, 1), -- Dyson vacuum
(4, 14, 1), -- Instant Pot

-- David Brown's cart
(5, 16, 1), -- Treadmill
(5, 18, 1), -- Backpack

-- Lisa Garcia's cart
(6, 19, 1), -- Olaplex
(6, 20, 2), -- Vitamins

-- Tom Anderson's cart
(7, 21, 1), -- LEGO set
(7, 22, 1), -- Nintendo Switch

-- Emma Taylor's cart
(8, 2, 1),  -- Samsung phone
(8, 6, 2);  -- Jeans

-- ==========================================
-- ORDERS SEED DATA
-- ==========================================
INSERT INTO orders (user_id, total_amount, status, shipping_address, billing_address, payment_method, notes) VALUES
(3, 1399.98, 'delivered', 
 '{"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001", "country": "USA"}',
 '{"street": "123 Main St", "city": "New York", "state": "NY", "zip": "10001", "country": "USA"}',
 'credit_card', 'Leave at front door'),
 
(4, 199.98, 'shipped',
 '{"street": "456 Oak Ave", "city": "Los Angeles", "state": "CA", "zip": "90210", "country": "USA"}',
 '{"street": "456 Oak Ave", "city": "Los Angeles", "state": "CA", "zip": "90210", "country": "USA"}',
 'paypal', 'Call before delivery'),
 
(5, 2399.98, 'processing',
 '{"street": "789 Pine Rd", "city": "Chicago", "state": "IL", "zip": "60601", "country": "USA"}',
 '{"street": "789 Pine Rd", "city": "Chicago", "state": "IL", "zip": "60601", "country": "USA"}',
 'credit_card', NULL),
 
(6, 839.98, 'confirmed',
 '{"street": "321 Elm St", "city": "Houston", "state": "TX", "zip": "77001", "country": "USA"}',
 '{"street": "321 Elm St", "city": "Houston", "state": "TX", "zip": "77001", "country": "USA"}',
 'debit_card', 'Fragile items'),
 
(7, 1649.98, 'pending',
 '{"street": "654 Maple Dr", "city": "Phoenix", "state": "AZ", "zip": "85001", "country": "USA"}',
 '{"street": "654 Maple Dr", "city": "Phoenix", "state": "AZ", "zip": "85001", "country": "USA"}',
 'credit_card', NULL);

-- ==========================================
-- ORDER ITEMS SEED DATA
-- ==========================================
INSERT INTO order_items (order_id, product_id, quantity, unit_price, total_price) VALUES
-- Order 1 (John Doe - delivered)
(1, 1, 1, 999.99, 999.99),  -- iPhone 15 Pro
(1, 4, 1, 399.99, 399.99),  -- Sony headphones

-- Order 2 (Jane Smith - shipped)
(2, 7, 1, 119.99, 119.99),  -- Nike shoes
(2, 8, 1, 79.99, 79.99),    -- Adidas hoodie

-- Order 3 (Mike Johnson - processing)
(3, 3, 1, 1199.99, 1199.99), -- MacBook Air
(3, 5, 1, 1199.99, 1199.99), -- iPad Pro (price was 1099.99 but captured at order time)

-- Order 4 (Sarah Wilson - confirmed)
(4, 13, 1, 749.99, 749.99), -- Dyson vacuum
(4, 14, 1, 89.99, 89.99),   -- Instant Pot

-- Order 5 (David Brown - pending)
(5, 16, 1, 1299.99, 1299.99), -- Treadmill
(5, 17, 1, 349.99, 349.99);   -- Yeti cooler

-- ==========================================
-- REVIEWS SEED DATA
-- ==========================================
INSERT INTO reviews (user_id, product_id, rating, title, comment, is_verified, is_approved) VALUES
-- iPhone 15 Pro reviews
(4, 1, 5, 'Amazing phone!', 'The camera quality is incredible and the battery life is excellent. Highly recommended!', TRUE, TRUE),
(5, 1, 4, 'Great upgrade', 'Coming from iPhone 12, this is a significant improvement. The titanium build feels premium.', TRUE, TRUE),
(6, 1, 5, 'Worth every penny', 'Best iPhone yet. The Action Button is a game changer.', TRUE, TRUE),

-- Samsung Galaxy S24 reviews
(3, 2, 4, 'Solid Android phone', 'Great performance and the AI features are actually useful. Camera is top-notch.', TRUE, TRUE),
(7, 2, 5, 'Love the display', 'The screen is absolutely gorgeous. Colors are vibrant and brightness is perfect even in sunlight.', TRUE, TRUE),

-- MacBook Air M3 reviews
(8, 3, 5, 'Perfect for work', 'Silent operation, incredible battery life, and the M3 chip handles everything I throw at it.', TRUE, TRUE),
(4, 3, 4, 'Great laptop', 'Very fast and the build quality is excellent. A bit expensive but worth it.', TRUE, TRUE),

-- Sony WH-1000XM5 reviews
(3, 4, 5, 'Best headphones ever', 'The noise cancellation is unreal. Perfect for flights and commuting.', TRUE, TRUE),
(9, 4, 4, 'Excellent sound quality', 'Music sounds amazing and they are very comfortable for long listening sessions.', TRUE, TRUE),

-- Nike Air Force 1 reviews
(10, 7, 4, 'Classic sneakers', 'Comfortable and goes with everything. True to size.', TRUE, TRUE),
(5, 7, 5, 'My favorite shoes', 'Have multiple pairs. They never go out of style and are super comfortable.', TRUE, TRUE),

-- Book reviews
(6, 10, 5, 'Life-changing book', 'Changed my perspective on money and investing. Easy to read and very practical.', TRUE, TRUE),
(7, 11, 5, 'Must read!', 'The best book on building habits. Implemented many strategies from this book.', TRUE, TRUE),
(8, 12, 4, 'Great for developers', 'Essential reading for any programmer. Helps write better, cleaner code.', TRUE, TRUE),

-- Home & Garden reviews
(9, 13, 5, 'Best vacuum ever', 'Picks up everything and the laser makes it easy to see dust. Battery life is great.', TRUE, TRUE),
(10, 14, 4, 'Love this cooker', 'Makes cooking so much easier. The preset programs work perfectly.', TRUE, TRUE),

-- LEGO reviews
(3, 21, 5, 'Amazing build experience', 'Took me 6 hours to complete but every minute was enjoyable. Display piece looks fantastic.', TRUE, TRUE),

-- Nintendo Switch reviews
(4, 22, 5, 'Perfect gaming console', 'The OLED screen is beautiful. Perfect for both docked and handheld gaming.', TRUE, TRUE);

-- ==========================================
-- UPDATE SEQUENCES (if needed)
-- ==========================================
-- Reset sequences to avoid conflicts
SELECT setval('users_id_seq', (SELECT MAX(id) FROM users));
SELECT setval('categories_id_seq', (SELECT MAX(id) FROM categories));
SELECT setval('products_id_seq', (SELECT MAX(id) FROM products));
SELECT setval('product_images_id_seq', (SELECT MAX(id) FROM product_images));
SELECT setval('carts_id_seq', (SELECT MAX(id) FROM carts));
SELECT setval('cart_items_id_seq', (SELECT MAX(id) FROM cart_items));
SELECT setval('orders_id_seq', (SELECT MAX(id) FROM orders));
SELECT setval('order_items_id_seq', (SELECT MAX(id) FROM order_items));
SELECT setval('reviews_id_seq', (SELECT MAX(id) FROM reviews));

-- ==========================================
-- REFRESH MATERIALIZED VIEWS
-- ==========================================
REFRESH MATERIALIZED VIEW popular_products;

-- ==========================================
-- VERIFICATION QUERIES
-- ==========================================
-- Run these to verify seed data
/*
SELECT 'Users' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Categories', COUNT(*) FROM categories
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Product Images', COUNT(*) FROM product_images
UNION ALL
SELECT 'Carts', COUNT(*) FROM carts
UNION ALL
SELECT 'Cart Items', COUNT(*) FROM cart_items
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items
UNION ALL
SELECT 'Reviews', COUNT(*) FROM reviews;
*/

-- End of seed data
