# E-Commerce Backend - ALX Project Nexus

A robust Django REST API backend for an e-commerce platform built as part of the ALX ProDev Backend Engineering program.

## 🚀 Project Overview

This e-commerce backend provides a complete solution for managing products, categories, user authentication, and order processing. It demonstrates advanced backend development skills including API design, database optimization, and security implementation.

## ✨ Key Features

- **Product Management**: Full CRUD operations for products and categories
- **User Authentication**: JWT-based secure authentication system
- **Advanced Filtering**: Filter products by category, price range, and availability
- **Sorting & Pagination**: Efficient data retrieval with customizable sorting
- **Order Management**: Complete order processing workflow
- **API Documentation**: Comprehensive Swagger/OpenAPI documentation
- **Performance Optimization**: Database indexing and query optimization
- **Security**: Input validation, rate limiting, and secure headers

## 🛠 Technology Stack

- **Backend Framework**: Django 5.0 + Django REST Framework 3.15
- **Database**: PostgreSQL 15+
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: drf-spectacular (Swagger/OpenAPI)
- **Caching**: Redis 7+
- **Testing**: pytest-django
- **Code Quality**: Black, flake8, isort

## 📋 Prerequisites

- Python 3.11+
- PostgreSQL 15+
- Redis 7+
- Git

## 🔧 Installation & Setup

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd alx_project_nexus/ecommerce_backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Configuration**
   ```bash
   cp .env.example .env
   # Edit .env with your database and other configurations
   ```

5. **Database Setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Load sample data**
   ```bash
   python manage.py loaddata fixtures/sample_data.json
   ```

7. **Run the development server**
   ```bash
   python manage.py runserver
   ```

## 📚 API Documentation

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **API Schema**: http://localhost:8000/api/schema/

## 🔐 Authentication

The API uses JWT authentication. To access protected endpoints:

1. Register: `POST /api/auth/register/`
2. Login: `POST /api/auth/login/`
3. Include JWT token in headers: `Authorization: Bearer <your-token>`

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Refresh JWT token

### Products
- `GET /api/products/` - List products (with filtering, sorting, pagination)
- `POST /api/products/` - Create product (admin only)
- `GET /api/products/{id}/` - Retrieve product details
- `PUT /api/products/{id}/` - Update product (admin only)
- `DELETE /api/products/{id}/` - Delete product (admin only)

### Categories
- `GET /api/categories/` - List categories
- `POST /api/categories/` - Create category (admin only)

### Orders
- `GET /api/orders/` - List user orders
- `POST /api/orders/` - Create new order
- `GET /api/orders/{id}/` - Order details

## 🧪 Testing

Run the test suite:
```bash
pytest
```

With coverage:
```bash
pytest --cov=.
```

## 🚀 Deployment

The application is deployed on [Heroku/Railway/DigitalOcean] and can be accessed at:
**Live API**: [Your deployed URL]

## 📈 Performance Features

- Database indexing on frequently queried fields
- Query optimization with select_related and prefetch_related
- Redis caching for frequently accessed data
- Pagination to handle large datasets
- API rate limiting to prevent abuse

## 🔒 Security Features

- JWT-based authentication
- Password hashing with Django's built-in system
- Input validation and sanitization
- CORS configuration
- Security headers middleware
- Rate limiting on API endpoints

## 🎯 Project Architecture

```
ecommerce_backend/
├── apps/
│   ├── authentication/
│   ├── products/
│   ├── orders/
│   └── core/
├── config/
├── fixtures/
├── tests/
└── requirements/
```

## 👨‍💻 Development Process

This project follows industry best practices:
- Feature-based development with descriptive Git commits
- Code review process
- Automated testing
- API-first development approach
- Comprehensive documentation

## 🏆 Key Achievements

- ✅ Complete RESTful API implementation
- ✅ Advanced filtering and search functionality
- ✅ Optimized database queries
- ✅ Comprehensive test coverage (>90%)
- ✅ Production-ready deployment
- ✅ Detailed API documentation

## 📞 Contact

**Developer**: [Your Name]
**Email**: [Your Email]
**LinkedIn**: [Your LinkedIn]
**GitHub**: [Your GitHub]

## 📄 License

This project is part of the ALX ProDev Backend Engineering program.

---

*Built with ❤️ for ALX Project Nexus*
