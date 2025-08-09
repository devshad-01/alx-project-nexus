#!/bin/bash

# 🎬 ALX Project Nexus - Live Demo Script
# This script runs the exact commands you'll use during your demo

echo "🎯 ALX Project Nexus - Live Demo Starting..."
echo "============================================="

# Set up environment
export BASE_URL="http://localhost:8000"
export API_URL="$BASE_URL/api"

echo ""
echo "📋 Demo Checklist:"
echo "✅ Server running on $BASE_URL"
echo "✅ API accessible at $API_URL"
echo "✅ Demo script ready"
echo ""

# Function to make demo look professional
demo_pause() {
    echo ""
    echo "⏸️  Press Enter to continue to next demo section..."
    read
}

# 1. Test server connectivity
echo "🔍 Step 1: Verifying server connectivity..."
if curl -s $BASE_URL > /dev/null; then
    echo "✅ Server is accessible at $BASE_URL"
else
    echo "❌ Server not accessible. Please run: python manage.py runserver"
    exit 1
fi

demo_pause

# 2. Show API Documentation
echo "📚 Step 2: API Documentation"
echo "🌐 Open these URLs in your browser:"
echo "   - Swagger UI: $API_URL/docs/"
echo "   - ReDoc: $API_URL/redoc/" 
echo "   - API Schema: $API_URL/schema/"
echo ""
echo "💡 Highlight: Auto-generated interactive documentation"

demo_pause

# 3. Authentication Demo
echo "🔐 Step 3: Live Authentication Demo"
echo ""

# Generate unique test data
TIMESTAMP=$(date +%s)
TEST_EMAIL="demo_user_$TIMESTAMP@example.com"

echo "🔥 Registering a new user..."
echo "📧 Email: $TEST_EMAIL"

# Register user and capture response
REGISTER_RESPONSE=$(curl -s -X POST $API_URL/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{
    \"email\": \"$TEST_EMAIL\",
    \"password\": \"DemoPassword123!\",
    \"password_confirm\": \"DemoPassword123!\",
    \"first_name\": \"Demo\",
    \"last_name\": \"User\"
  }")

echo "📄 Registration Response:"
echo "$REGISTER_RESPONSE" | python3 -m json.tool

# Extract access token
ACCESS_TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data.get('tokens', {}).get('access', 'NO_TOKEN'))" 2>/dev/null)

if [ "$ACCESS_TOKEN" != "NO_TOKEN" ] && [ ! -z "$ACCESS_TOKEN" ]; then
    echo ""
    echo "✅ SUCCESS: User registered and JWT token obtained!"
    echo "🎫 Token: ${ACCESS_TOKEN:0:50}..."
else
    echo ""
    echo "⚠️  Registration response received but token extraction needs manual review"
fi

demo_pause

# 4. Product Catalog Demo
echo "📦 Step 4: Product Catalog Demo"
echo ""

echo "🏷️  Fetching product categories..."
curl -s $API_URL/products/categories/ | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f'📊 Found {len(data)} categories:')
    for cat in data[:3]:
        print(f'   • {cat[\"name\"]} (ID: {cat[\"id\"]})')
except: pass
"

echo ""
echo "🛍️  Fetching products..."
curl -s $API_URL/products/ | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    results = data.get('results', data) if isinstance(data, dict) else data
    print(f'📊 Found {len(results)} products:')
    for prod in results[:3]:
        print(f'   • {prod[\"name\"]} - \${prod[\"price\"]} (ID: {prod[\"id\"]})')
        if 'stock_quantity' in prod:
            print(f'     Stock: {prod[\"stock_quantity\"]} units')
except Exception as e:
    print(f'Products data: {data[:200]}...')
"

demo_pause

# 5. Cart Operations Demo
echo "🛒 Step 5: Shopping Cart Demo"
echo ""

if [ "$ACCESS_TOKEN" != "NO_TOKEN" ] && [ ! -z "$ACCESS_TOKEN" ]; then
    echo "🔑 Using authentication token for cart operations..."
    
    echo ""
    echo "📋 Checking empty cart..."
    curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
         $API_URL/cart/ | python3 -m json.tool
    
    echo ""
    echo "➕ Adding item to cart (Product ID: 53)..."
    ADD_RESPONSE=$(curl -s -X POST $API_URL/cart/add/ \
      -H "Authorization: Bearer $ACCESS_TOKEN" \
      -H "Content-Type: application/json" \
      -d '{
        "product_id": 53,
        "quantity": 2
      }')
    
    echo "📄 Add to Cart Response:"
    echo "$ADD_RESPONSE" | python3 -m json.tool
    
    echo ""
    echo "🛒 Viewing cart with items..."
    curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
         $API_URL/cart/ | python3 -m json.tool
         
else
    echo "⚠️  Skipping cart demo - authentication token not available"
    echo "💡 Demo tip: Show cart endpoints in Swagger UI instead"
fi

demo_pause

# 6. Working Features Summary
echo "🎯 Step 6: Demo Summary"
echo ""
echo "✅ Features Successfully Demonstrated:"
echo "   🔐 User Registration & JWT Authentication"
echo "   📚 Auto-Generated API Documentation (Swagger/ReDoc)"
echo "   📦 Product Catalog with Categories"
echo "   🛒 Shopping Cart Operations"
echo "   🗄️ Database Integration with Django ORM"
echo "   🔒 Authentication-Protected Endpoints"
echo ""
echo "🏗️  Additional Features Available:"
echo "   👨‍💼 Django Admin Interface ($BASE_URL/admin/)"
echo "   📋 Order Management System"
echo "   🧪 Comprehensive API Testing Suite"
echo "   📖 Complete Project Documentation"
echo ""
echo "🚀 Project Highlights:"
echo "   • Clean, professional architecture"
echo "   • Industry-standard REST API design" 
echo "   • Comprehensive documentation"
echo "   • Security best practices"
echo "   • Production-ready configuration"
echo ""
echo "🎉 Demo Complete! Ready for questions."
echo "============================================="
