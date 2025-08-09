"""
Comprehensive seed data management command for ALX Project Nexus E-Commerce Backend
Creates realistic test data for all models with proper relationships
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from authentication.models import User
from products.models import Category, Product, ProductImage, Review
from orders.models import Order, OrderItem
from core.models import Cart, CartItem
from decimal import Decimal
import random
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed the database with comprehensive test data for e-commerce platform'

    def add_arguments(self, parser):
        parser.add_argument(
            '--mode',
            type=str,
            choices=['basic', 'full', 'demo'],
            default='basic',
            help='Seeding mode: basic (minimal), full (comprehensive), demo (showcase data)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding'
        )

    def handle(self, *args, **options):
        mode = options['mode']
        clear_data = options.get('clear', False)

        self.stdout.write(
            self.style.SUCCESS(f'🌱 Starting seed process in {mode.upper()} mode...')
        )

        try:
            with transaction.atomic():
                if clear_data:
                    self.clear_existing_data()
                
                if mode == 'basic':
                    self.seed_basic_data()
                elif mode == 'full':
                    self.seed_full_data()
                elif mode == 'demo':
                    self.seed_demo_data()
                
                self.stdout.write(
                    self.style.SUCCESS('✅ Seeding completed successfully!')
                )
                self.display_summary()
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'❌ Seeding failed: {str(e)}')
            )
            raise CommandError(f'Seeding failed: {str(e)}')

    def clear_existing_data(self):
        """Clear existing data in proper order to avoid foreign key constraints"""
        self.stdout.write('🧹 Clearing existing data...')
        
        # Clear in reverse dependency order
        CartItem.objects.all().delete()
        OrderItem.objects.all().delete()
        Review.objects.all().delete()
        ProductImage.objects.all().delete()
        Order.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Cart.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()  # Keep superuser
        
        self.stdout.write(self.style.WARNING('   Data cleared successfully'))

    def seed_basic_data(self):
        """Create minimal data for basic testing"""
        self.stdout.write('🏗️  Creating basic test data...')
        
        # Create 2 test users
        users = self.create_users(2)
        
        # Create 3 categories
        categories = self.create_categories([
            'Electronics',
            'Clothing',
            'Books'
        ])
        
        # Create 6 products (2 per category)
        products = []
        for category in categories:
            products.extend(self.create_products_for_category(category, 2))
        
        # Create product images for all products
        for product in products:
            self.create_product_images(product, 1)
        
        # Create 2 orders
        orders = self.create_orders(users[:2])
        
        # Create reviews
        self.create_reviews(users, products[:4])

    def seed_full_data(self):
        """Create comprehensive data for full testing"""
        self.stdout.write('🏗️  Creating comprehensive test data...')
        
        # Create 10 test users
        users = self.create_users(10)
        
        # Create 8 categories
        categories = self.create_categories([
            'Electronics',
            'Clothing',
            'Books',
            'Home & Garden',
            'Sports & Outdoors',
            'Health & Beauty',
            'Toys & Games',
            'Automotive'
        ])
        
        # Create 40 products (5 per category)
        products = []
        for category in categories:
            products.extend(self.create_products_for_category(category, 5))
        
        # Create product images (2-3 per product)
        for product in products:
            self.create_product_images(product, random.randint(2, 3))
        
        # Create 15 orders
        orders = self.create_orders(users[:8])
        
        # Create reviews for 60% of products
        review_products = random.sample(products, int(len(products) * 0.6))
        self.create_reviews(users, review_products)
        
        # Add items to some carts
        self.populate_carts(users[:5], products)

    def seed_demo_data(self):
        """Create showcase data for demonstrations"""
        self.stdout.write('🏗️  Creating demo showcase data...')
        
        # Create realistic demo users
        demo_users = [
            ('john.doe@example.com', 'johndoe', 'John', 'Doe'),
            ('jane.smith@example.com', 'janesmith', 'Jane', 'Smith'),
            ('mike.johnson@example.com', 'mikejohnson', 'Mike', 'Johnson'),
            ('sarah.wilson@example.com', 'sarahwilson', 'Sarah', 'Wilson'),
            ('david.brown@example.com', 'davidbrown', 'David', 'Brown'),
        ]
        
        users = []
        for email, username, first_name, last_name in demo_users:
            user = User.objects.create_user(
                username=username,
                email=email,
                first_name=first_name,
                last_name=last_name,
                password='demo123'
            )
            users.append(user)
            self.stdout.write(f'   👤 Created demo user: {user.email}')
        
        # Create curated categories with descriptions
        category_data = [
            ('Electronics', 'Latest smartphones, laptops, and tech gadgets'),
            ('Fashion', 'Trendy clothing and accessories for all occasions'),
            ('Books', 'Educational and entertainment books for all ages'),
            ('Home Decor', 'Beautiful items to make your house a home'),
        ]
        
        categories = []
        for name, description in category_data:
            category = Category.objects.create(
                name=name,
                description=description,
                is_active=True
            )
            categories.append(category)
            self.stdout.write(f'   📁 Created category: {category.name}')
        
        # Create premium demo products
        self.create_premium_demo_products(categories, users[0])
        
        # Create realistic orders
        self.create_demo_orders(users)

    def create_users(self, count):
        """Create test users"""
        users = []
        for i in range(count):
            user = User.objects.create_user(
                username=f'testuser{i+1}',
                email=f'testuser{i+1}@example.com',
                first_name=f'Test{i+1}',
                last_name='User',
                password='testpass123'
            )
            users.append(user)
        
        self.stdout.write(f'   👥 Created {count} users')
        return users

    def create_categories(self, category_names):
        """Create product categories"""
        categories = []
        for name in category_names:
            category, created = Category.objects.get_or_create(
                name=name,
                defaults={
                    'description': f'High-quality {name.lower()} for all your needs',
                    'is_active': True
                }
            )
            categories.append(category)
        
        self.stdout.write(f'   📁 Created {len(categories)} categories')
        return categories

    def create_products_for_category(self, category, count):
        """Create products for a specific category"""
        products = []
        
        # Product templates by category
        product_templates = {
            'Electronics': [
                ('iPhone 15 Pro', 'Latest iPhone with advanced camera', Decimal('999.99')),
                ('MacBook Pro', 'Powerful laptop for professionals', Decimal('1999.99')),
                ('Samsung Galaxy S24', 'Android flagship smartphone', Decimal('899.99')),
                ('iPad Air', 'Versatile tablet for work and play', Decimal('599.99')),
                ('AirPods Pro', 'Wireless earbuds with noise cancellation', Decimal('249.99')),
            ],
            'Clothing': [
                ('Premium Cotton T-Shirt', 'Comfortable everyday wear', Decimal('29.99')),
                ('Designer Jeans', 'Stylish denim for any occasion', Decimal('79.99')),
                ('Winter Jacket', 'Warm and waterproof outerwear', Decimal('149.99')),
                ('Running Shoes', 'High-performance athletic footwear', Decimal('119.99')),
                ('Casual Dress', 'Elegant dress for special occasions', Decimal('89.99')),
            ],
            'Books': [
                ('Python Programming Guide', 'Complete guide to Python development', Decimal('49.99')),
                ('Mystery Novel', 'Thrilling page-turner mystery', Decimal('19.99')),
                ('Cookbook Collection', 'International recipes for home cooks', Decimal('34.99')),
                ('Science Textbook', 'Comprehensive science education', Decimal('89.99')),
                ('Art History Book', 'Beautiful exploration of world art', Decimal('59.99')),
            ]
        }
        
        # Default template for other categories
        default_templates = [
            (f'{category.name} Item 1', f'High-quality {category.name.lower()} product', Decimal('99.99')),
            (f'{category.name} Item 2', f'Premium {category.name.lower()} solution', Decimal('149.99')),
            (f'{category.name} Item 3', f'Essential {category.name.lower()} accessory', Decimal('79.99')),
            (f'{category.name} Item 4', f'Professional {category.name.lower()} tool', Decimal('199.99')),
            (f'{category.name} Item 5', f'Deluxe {category.name.lower()} package', Decimal('299.99')),
        ]
        
        templates = product_templates.get(category.name, default_templates)
        
        for i in range(count):
            if i < len(templates):
                name, description, price = templates[i]
            else:
                name = f'{category.name} Product {i+1}'
                description = f'Quality {category.name.lower()} product for all your needs'
                price = Decimal(random.uniform(19.99, 299.99))
            
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                category=category,
                sku=f'{category.name[:3].upper()}{i+1:03d}',
                stock_quantity=random.randint(10, 100),
                is_active=True,
                is_featured=random.choice([True, False])
            )
            products.append(product)
        
        return products

    def create_product_images(self, product, count):
        """Create product images"""
        for i in range(count):
            ProductImage.objects.create(
                product=product,
                image_url=f'https://via.placeholder.com/600x400?text={product.name.replace(" ", "+")}+Image+{i+1}',
                alt_text=f'{product.name} - Image {i+1}',
                is_primary=(i == 0),
                sort_order=i
            )

    def create_orders(self, users):
        """Create test orders"""
        orders = []
        for user in users:
            # Create 1-3 orders per user
            order_count = random.randint(1, 3)
            for _ in range(order_count):
                order = Order.objects.create(
                    user=user,
                    total_amount=Decimal(random.uniform(50.00, 500.00)),
                    status=random.choice(['pending', 'confirmed', 'processing', 'shipped']),
                    shipping_address={
                        'street': f'{random.randint(100, 999)} Main St',
                        'city': random.choice(['Nairobi', 'Mombasa', 'Kisumu', 'Nakuru']),
                        'country': 'Kenya'
                    },
                    payment_method=random.choice(['Credit Card', 'PayPal', 'Bank Transfer'])
                )
                orders.append(order)
        
        self.stdout.write(f'   📦 Created {len(orders)} orders')
        return orders

    def create_reviews(self, users, products):
        """Create product reviews"""
        review_count = 0
        for product in products:
            # 30-70% chance each product gets reviews
            if random.random() < 0.5:
                continue
                
            # 1-3 reviews per product
            num_reviews = random.randint(1, 3)
            review_users = random.sample(users, min(num_reviews, len(users)))
            
            for user in review_users:
                Review.objects.create(
                    user=user,
                    product=product,
                    rating=random.randint(3, 5),  # Mostly positive reviews
                    title=random.choice([
                        'Great product!',
                        'Excellent quality',
                        'Highly recommended',
                        'Good value for money',
                        'Fast delivery'
                    ]),
                    comment=random.choice([
                        'Very satisfied with this purchase. Great quality!',
                        'Exactly what I was looking for. Fast shipping too.',
                        'Good product, would buy again.',
                        'Excellent customer service and product quality.',
                        'Perfect for my needs. Highly recommend!'
                    ]),
                    is_approved=True,
                    is_verified=random.choice([True, False])
                )
                review_count += 1
        
        self.stdout.write(f'   ⭐ Created {review_count} reviews')

    def populate_carts(self, users, products):
        """Add items to user carts"""
        for user in users:
            # Add 1-4 items to each cart
            cart_products = random.sample(products, random.randint(1, 4))
            for product in cart_products:
                CartItem.objects.create(
                    cart=user.cart,
                    product=product,
                    quantity=random.randint(1, 3)
                )
        
        self.stdout.write(f'   🛒 Populated {len(users)} shopping carts')

    def create_premium_demo_products(self, categories, creator_user):
        """Create high-quality demo products for showcase"""
        premium_products = [
            {
                'name': 'iPhone 15 Pro Max',
                'description': 'The ultimate iPhone with titanium design, advanced camera system, and A17 Pro chip',
                'price': Decimal('1199.99'),
                'category': categories[0],  # Electronics
                'stock': 25,
                'featured': True
            },
            {
                'name': 'Designer Leather Jacket',
                'description': 'Premium genuine leather jacket with contemporary styling and superior craftsmanship',
                'price': Decimal('299.99'),
                'category': categories[1],  # Fashion
                'stock': 15,
                'featured': True
            },
            {
                'name': 'Complete Python Programming Course',
                'description': 'Comprehensive guide from beginner to advanced Python programming with real projects',
                'price': Decimal('79.99'),
                'category': categories[2],  # Books
                'stock': 100,
                'featured': False
            },
            {
                'name': 'Modern Minimalist Sofa',
                'description': 'Elegant 3-seater sofa with premium fabric upholstery and solid wood frame',
                'price': Decimal('899.99'),
                'category': categories[3],  # Home Decor
                'stock': 8,
                'featured': True
            }
        ]
        
        for product_data in premium_products:
            product = Product.objects.create(
                name=product_data['name'],
                description=product_data['description'],
                price=product_data['price'],
                category=product_data['category'],
                sku=f"DEMO{random.randint(1000, 9999)}",
                stock_quantity=product_data['stock'],
                is_active=True,
                is_featured=product_data['featured'],
                created_by=creator_user
            )
            
            # Add multiple high-quality images
            self.create_product_images(product, 3)
            
            self.stdout.write(f'   🌟 Created premium product: {product.name}')

    def create_demo_orders(self, users):
        """Create realistic demo orders with proper order items"""
        orders_data = [
            {
                'user': users[0],
                'status': 'delivered',
                'total': Decimal('1199.99'),
                'shipping': {
                    'street': '123 Tech Avenue',
                    'city': 'Nairobi',
                    'country': 'Kenya'
                }
            },
            {
                'user': users[1],
                'status': 'shipped',
                'total': Decimal('379.98'),
                'shipping': {
                    'street': '456 Fashion Street',
                    'city': 'Mombasa',
                    'country': 'Kenya'
                }
            },
            {
                'user': users[2],
                'status': 'processing',
                'total': Decimal('79.99'),
                'shipping': {
                    'street': '789 Book Lane',
                    'city': 'Kisumu',
                    'country': 'Kenya'
                }
            }
        ]
        
        for order_data in orders_data:
            Order.objects.create(
                user=order_data['user'],
                total_amount=order_data['total'],
                status=order_data['status'],
                shipping_address=order_data['shipping'],
                payment_method='Credit Card'
            )
        
        self.stdout.write(f'   📦 Created {len(orders_data)} demo orders')

    def display_summary(self):
        """Display seeding summary"""
        self.stdout.write('\n📊 SEEDING SUMMARY:')
        self.stdout.write(f'   Users: {User.objects.count()}')
        self.stdout.write(f'   Categories: {Category.objects.count()}')
        self.stdout.write(f'   Products: {Product.objects.count()}')
        self.stdout.write(f'   Product Images: {ProductImage.objects.count()}')
        self.stdout.write(f'   Orders: {Order.objects.count()}')
        self.stdout.write(f'   Order Items: {OrderItem.objects.count()}')
        self.stdout.write(f'   Reviews: {Review.objects.count()}')
        self.stdout.write(f'   Carts: {Cart.objects.count()}')
        self.stdout.write(f'   Cart Items: {CartItem.objects.count()}')
        
        self.stdout.write('\n🎯 ADMIN ACCESS:')
        self.stdout.write('   URL: http://127.0.0.1:8000/admin/')
        self.stdout.write('   Username: admin')
        self.stdout.write('   Password: admin123')
        
        self.stdout.write('\n🚀 Ready for testing and development!')
