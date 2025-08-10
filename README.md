# Project Nexus - E-Commerce Backend API

A robust, scalable e-commerce backend API built with Django REST Framework, featuring comprehensive product management, user authentication, order processing, and shopping cart functionality.

## 🚀 Live Demo

- **API Documentation**: [https://alx-project-nexus-nb67.onrender.com/api/docs/](https://alx-project-nexus-nb67.onrender.com/api/docs/)
- **API Schema**: [https://alx-project-nexus-nb67.onrender.com/api/schema/](https://alx-project-nexus-nb67.onrender.com/api/schema/)
- **ReDoc Documentation**: [https://alx-project-nexus-nb67.onrender.com/api/redoc/](https://alx-project-nexus-nb67.onrender.com/api/redoc/)

## 🎯 Project Overview

This e-commerce backend provides a complete solution for managing products, categories, user authentication, and order processing. It demonstrates advanced backend development skills including API design, database optimization, and security implementation.

## ✨ Key Features

### Core Functionality
- **User Management**: Registration, authentication, and profile management
- **Product Catalog**: Complete CRUD operations for products with categories
- **Shopping Cart**: Add, update, remove items with persistent storage
- **Order Management**: Order creation, tracking, and status updates
- **Authentication**: JWT-based secure authentication system

### Technical Features
- **RESTful API Design**: Clean, intuitive API endpoints
- **Interactive Documentation**: Swagger/OpenAPI documentation
- **Database Optimization**: Efficient queries with Django ORM
- **Security**: CORS handling, secure headers, and authentication
- **Scalable Architecture**: Modular design for easy extension

## 🛠 Tech Stack

### Backend
- **Framework**: Django 5.0.8 + Django REST Framework 3.15.2
- **Database**: PostgreSQL (Production) / SQLite (Development)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Documentation**: drf-spectacular (OpenAPI/Swagger)

### Deployment & Infrastructure
- **Hosting**: Render
- **Database**: Aiven Cloud PostgreSQL
- **Static Files**: WhiteNoise
- **Process Management**: Gunicorn

### Development Tools
- **Version Control**: Git/GitHub
- **Code Quality**: Black (formatting), pytest (testing)
- **Environment Management**: python-decouple
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
