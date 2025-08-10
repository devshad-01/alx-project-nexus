#!/usr/bin/env python
"""
Create test data ...dummy daTa
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')
django.setup()

from django.contrib.auth import get_user_model
from products.models import Category, Product
from core.models import Cart

User = get_user_model()

def create_test_data():
    print("🚀 Creating test data for demonstration...")
    
    # Create test user
    if not User.objects.filter(email='demo@example.com').exists():
        user = User.objects.create_user(
            username='demo_user',
            email='demo@example.com',
            password='testpass123',
            first_name='Demo',
            last_name='User'
        )
        print(f"✅ Created demo user: {user.email}")
    else:
        user = User.objects.get(email='demo@example.com')
        print(f"✅ Demo user already exists: {user.email}")
    
    # Create categories
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
        {'name': 'Clothing', 'description': 'Fashion and apparel'},
        {'name': 'Books', 'description': 'Books and literature'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults={'description': cat_data['description']}
        )
        if created:
            print(f"✅ Created category: {category.name}")
        else:
            print(f"✅ Category already exists: {category.name}")
    
    # Create products
    electronics = Category.objects.get(name='Electronics')
    clothing = Category.objects.get(name='Clothing')
    books = Category.objects.get(name='Books')
    
    products_data = [
        {
            'name': 'iPhone 15 Pro',
            'description': 'Latest Apple smartphone with advanced features',
            'price': 999.99,
            'stock_quantity': 50,
            'category': electronics,
            'sku': 'PHONE001'
        },
        {
            'name': 'MacBook Air M2',
            'description': 'Powerful laptop for professionals',
            'price': 1299.99,
            'stock_quantity': 30,
            'category': electronics,
            'sku': 'LAPTOP001'
        },
        {
            'name': 'Classic T-Shirt',
            'description': 'Comfortable cotton t-shirt',
            'price': 29.99,
            'stock_quantity': 100,
            'category': clothing,
            'sku': 'SHIRT001'
        },
        {
            'name': 'Python Programming Book',
            'description': 'Learn Python programming from basics to advanced',
            'price': 49.99,
            'stock_quantity': 75,
            'category': books,
            'sku': 'BOOK001'
        }
    ]
    
    for prod_data in products_data:
        try:
            product, created = Product.objects.get_or_create(
                sku=prod_data['sku'],
                defaults=prod_data
            )
            if created:
                print(f"✅ Created product: {product.name}")
            else:
                print(f"✅ Product already exists: {product.name}")
        except Exception as e:
            # If there's a duplicate slug, try to find existing product
            try:
                product = Product.objects.get(sku=prod_data['sku'])
                print(f"✅ Product already exists: {product.name}")
            except Product.DoesNotExist:
                print(f"⚠️ Could not create product {prod_data['name']}: {e}")
    
    print("\n🎉 Test data creation completed!")
    print(f"📊 Total Users: {User.objects.count()}")
    print(f"📊 Total Categories: {Category.objects.count()}")
    print(f"📊 Total Products: {Product.objects.count()}")
    print("\n🔗 You can now test these endpoints:")
    print("   GET http://localhost:8000/api/products/")
    print("   GET http://localhost:8000/api/products/categories/")
    print("   POST http://localhost:8000/api/auth/login/ (email: demo@example.com, password: testpass123)")
    print("   POST http://localhost:8000/api/auth/register/ (create new users)")
    print("   GET http://localhost:8000/api/orders/ (requires authentication)")
    print("   GET http://localhost:8000/api/cart/ (requires authentication)")

if __name__ == '__main__':
    create_test_data()
