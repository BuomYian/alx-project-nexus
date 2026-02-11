# E-Commerce Backend - ProDev Backend Engineering Project

## Overview

This project is a **real-world e-commerce backend application** developed as part of the ProDev Backend Engineering program. It simulates a production-level development environment, emphasizing **scalability, security, and performance**. The backend supports a comprehensive product catalog system with advanced filtering, sorting, and pagination capabilities.

## Real-World Application

The e-commerce backend serves as a practical learning ground where participants will:

✅ **Design and optimize** relational database schemas for high-performance queries  
✅ **Build and document** RESTful APIs for seamless frontend integration  
✅ **Enhance performance** through strategic query optimization and database indexing  
✅ **Implement security** measures with JWT authentication and authorization  
✅ **Document comprehensively** using OpenAPI/Swagger standards

---

## Project Goals

### 1. **CRUD APIs** 🔄

- Build complete Create, Read, Update, Delete operations for products and categories
- Implement user authentication and management features using JWT tokens
- Ensure data integrity and validation at the API level

### 2. **Advanced Filtering, Sorting & Pagination** 🔍

- Implement robust filtering logic for product discovery (by category, price range, attributes)
- Enable sorting by multiple criteria (price, date, popularity)
- Implement pagination for efficient handling of large datasets
- Optimize query performance for real-world scale

### 3. **Database Optimization** ⚡

- Design a high-performance relational database schema
- Implement strategic indexing on frequently queried columns
- Use database best practices for data normalization
- Monitor and optimize query execution plans

### 4. **API Documentation & Testing** 📚

- Generate API documentation using Swagger/OpenAPI
- Provide interactive API testing through documented endpoints
- Create clear usage examples for frontend integration

---

## Technologies Used

### Backend Framework

- **Django** (v3.2+): Full-featured web framework for building scalable APIs
- **Django REST Framework**: For building robust RESTful APIs
- **Python** (v3.9+): Core programming language

### Database

- **PostgreSQL**: Enterprise-grade relational database for optimized performance
- **SQLAlchemy/Django ORM**: For database abstraction and query building

### Authentication & Security

- **JWT (JSON Web Tokens)**: For stateless, secure user authentication
- **Django-CORS-Headers**: For handling cross-origin requests
- **Django-Filter**: For implementing advanced filtering

### API Documentation & Testing

- **Swagger/OpenAPI**: For interactive API documentation
- **DRF Spectacular**: Django REST Framework integration with OpenAPI
- **Postman**: For API testing and collection management

### Additional Tools

- **Git**: Version control and collaboration
- **Docker**: Containerization for consistent environments (optional)
- **Pytest**: Unit and integration testing framework

---

## Key Features

### 1️⃣ CRUD Operations

#### Products Management

```
POST   /api/products/              - Create a new product
GET    /api/products/              - List all products
GET    /api/products/<id>/         - Retrieve product details
PUT    /api/products/<id>/         - Update product information
DELETE /api/products/<id>/         - Delete a product
```

#### Categories Management

```
POST   /api/categories/            - Create a new category
GET    /api/categories/            - List all categories
GET    /api/categories/<id>/       - Retrieve category details
PUT    /api/categories/<id>/       - Update category information
DELETE /api/categories/<id>/       - Delete a category
```

#### User Authentication

```
POST   /api/auth/register/         - User registration
POST   /api/auth/login/            - User login
POST   /api/auth/refresh/          - Refresh JWT token
POST   /api/auth/logout/           - User logout
GET    /api/users/<id>/            - Retrieve user profile
PUT    /api/users/<id>/            - Update user profile
```

### 2️⃣ Advanced API Features

#### Filtering

- **By Category**: `/api/products/?category=electronics`
- **By Price Range**: `/api/products/?min_price=100&max_price=500`
- **By Attributes**: `/api/products/?brand=Sony&color=Black`
- **Text Search**: `/api/products/?search=smartphone`

#### Sorting

- **By Price**: `/api/products/?ordering=price` or `?ordering=-price`
- **By Popularity**: `/api/products/?ordering=-sales_count`
- **By Date**: `/api/products/?ordering=-created_at`
- **By Rating**: `/api/products/?ordering=-average_rating`

#### Pagination

- **Page-based**: `/api/products/?page=1&page_size=20`
- **Limit-Offset**: `/api/products/?limit=20&offset=0`
- **Cursor-based**: `/api/products/?cursor=cD00NQ==` (for large datasets)

### 3️⃣ API Documentation

- **Swagger UI**: Interactive API documentation at `/api/docs/`
- **ReDoc**: Alternative API documentation at `/api/redoc/`
- **OpenAPI Schema**: Machine-readable schema at `/api/schema/`
- **Postman Collection**: Exportable collection for testing

---

## Database Schema

### Key Tables

#### Users Table

```sql
users
├── id (PK)
├── username (UNIQUE)
├── email (UNIQUE)
├── password_hash
├── first_name
├── last_name
├── is_active
├── created_at
├── updated_at
└── last_login
```

#### Categories Table

```sql
categories
├── id (PK)
├── name (UNIQUE)
├── slug (UNIQUE)
├── description
├── parent_category_id (FK)
├── is_active
├── created_at
└── updated_at
```

#### Products Table

```sql
products
├── id (PK)
├── name
├── slug (UNIQUE)
├── description
├── sku (UNIQUE)
├── category_id (FK)
├── price
├── discount_price
├── quantity_in_stock
├── is_active
├── average_rating
├── sales_count
├── created_at
├── updated_at
└── created_by_id (FK)
```

#### Product Attributes Table

```sql
product_attributes
├── id (PK)
├── product_id (FK)
├── attribute_key
├── attribute_value
└── created_at
```

#### Reviews Table

```sql
reviews
├── id (PK)
├── product_id (FK)
├── user_id (FK)
├── rating (1-5)
├── title
├── comment
├── is_verified_purchase
├── created_at
└── updated_at
```

### Indexing Strategy

```sql
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_price ON products(price);
CREATE INDEX idx_products_is_active ON products(is_active);
CREATE INDEX idx_products_created_at ON products(created_at DESC);
CREATE INDEX idx_product_attributes_product_id ON product_attributes(product_id);
CREATE INDEX idx_reviews_product_id ON reviews(product_id);
CREATE INDEX idx_reviews_user_id ON reviews(user_id);
```

---

## Implementation Process

### Phase 1: Project Setup

- [ ] Initialize Django project with PostgreSQL
- [ ] Set up virtual environment and dependencies
- [ ] Configure environment variables and settings
- [ ] Initialize Git repository

### Phase 2: Database & Models

- [ ] Design database schema
- [ ] Create Django models for Users, Categories, Products, Reviews
- [ ] Implement model relationships and constraints
- [ ] Create database migrations
- [ ] Add strategic indexes for performance

### Phase 3: Authentication & Security

- [ ] Implement JWT authentication
- [ ] Create user registration and login endpoints
- [ ] Implement token refresh and logout logic
- [ ] Add permission classes and authentication decorators
- [ ] Secure endpoints with proper authorization checks

### Phase 4: Core CRUD APIs

- [ ] Implement Product CRUD operations
- [ ] Implement Category CRUD operations
- [ ] Add user profile management endpoints
- [ ] Implement input validation and error handling

### Phase 5: Advanced Features

- [ ] Implement filtering with django-filter
- [ ] Add sorting capabilities
- [ ] Implement pagination (page-based and cursor-based)
- [ ] Add search functionality
- [ ] Implement review and rating system

### Phase 6: Documentation & Testing

- [ ] Integrate DRF Spectacular for Swagger generation
- [ ] Add docstrings and inline documentation
- [ ] Create unit tests for models
- [ ] Create integration tests for APIs
- [ ] Generate API documentation

### Phase 7: Performance Optimization

- [ ] Analyze and optimize database queries
- [ ] Implement query result caching
- [ ] Add database connection pooling
- [ ] Monitor and log slow queries
- [ ] Implement rate limiting

### Phase 8: Deployment & Hosting

- [ ] Prepare for production deployment
- [ ] Set up CI/CD pipeline
- [ ] Deploy to hosting platform
- [ ] Publish API documentation
- [ ] Set up monitoring and alerting

---

## Git Commit Workflow

Follow this commit structure for organized version control:

```bash
# Project initialization
git commit -m "feat: initialize Django project with PostgreSQL configuration"

# Database setup
git commit -m "feat: create database models for users, products, and categories"
git commit -m "feat: add database indexes for query optimization"

# Authentication
git commit -m "feat: implement JWT authentication system"
git commit -m "feat: add user registration and login endpoints"

# Core APIs
git commit -m "feat: implement product CRUD APIs"
git commit -m "feat: implement category CRUD APIs"
git commit -m "feat: add user profile management endpoints"

# Advanced Features
git commit -m "feat: add filtering and sorting to product APIs"
git commit -m "feat: implement pagination for product listings"
git commit -m "feat: add product review and rating system"

# Performance
git commit -m "perf: optimize product list queries with select_related"
git commit -m "perf: add database indexes for frequently queried fields"
git commit -m "perf: implement result caching for product listings"

# Documentation
git commit -m "docs: integrate Swagger/OpenAPI documentation"
git commit -m "docs: add API usage examples in documentation"
git commit -m "docs: create deployment and setup instructions"

# Testing
git commit -m "test: add unit tests for models"
git commit -m "test: add integration tests for API endpoints"

# Bug fixes and improvements
git commit -m "fix: resolve filtering bug in product search"
git commit -m "refactor: improve error handling in authentication"
```

---

## API Endpoints Summary

### Authentication Endpoints

| Method | Endpoint              | Purpose                        |
| ------ | --------------------- | ------------------------------ |
| POST   | `/api/auth/register/` | User registration              |
| POST   | `/api/auth/login/`    | User login with JWT generation |
| POST   | `/api/auth/refresh/`  | Refresh JWT token              |
| POST   | `/api/auth/logout/`   | User logout                    |

### Product Endpoints

| Method | Endpoint              | Purpose                                      |
| ------ | --------------------- | -------------------------------------------- |
| GET    | `/api/products/`      | List products with filters, sort, pagination |
| POST   | `/api/products/`      | Create new product                           |
| GET    | `/api/products/{id}/` | Get product details                          |
| PUT    | `/api/products/{id}/` | Update product                               |
| DELETE | `/api/products/{id}/` | Delete product                               |

### Category Endpoints

| Method | Endpoint                | Purpose              |
| ------ | ----------------------- | -------------------- |
| GET    | `/api/categories/`      | List all categories  |
| POST   | `/api/categories/`      | Create new category  |
| GET    | `/api/categories/{id}/` | Get category details |
| PUT    | `/api/categories/{id}/` | Update category      |
| DELETE | `/api/categories/{id}/` | Delete category      |

### User Endpoints

| Method | Endpoint                  | Purpose             |
| ------ | ------------------------- | ------------------- |
| GET    | `/api/users/{id}/`        | Get user profile    |
| PUT    | `/api/users/{id}/`        | Update user profile |
| GET    | `/api/users/{id}/orders/` | Get user orders     |

### Review Endpoints

| Method | Endpoint                      | Purpose             |
| ------ | ----------------------------- | ------------------- |
| GET    | `/api/products/{id}/reviews/` | Get product reviews |
| POST   | `/api/products/{id}/reviews/` | Add product review  |
| PUT    | `/api/reviews/{id}/`          | Update review       |
| DELETE | `/api/reviews/{id}/`          | Delete review       |

---

## Submission Details

### API Deployment

- Host the API on a cloud platform (Heroku, DigitalOcean, AWS, Google Cloud, etc.)
- Ensure production-ready security configurations
- Publish comprehensive API documentation (Swagger/Postman)
- Provide base URL and authentication instructions

### Repository Structure

```
ecommerce-backend/
├── README.md
├── requirements.txt
├── manage.py
├── .env.example
├── .gitignore
├── docker-compose.yml (optional)
├── ecommerce_project/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── products/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── filters.py
│   └── tests.py
├── accounts/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── categories/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── urls.py
├── reviews/
│   ├── migrations/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   └── tests.py
└── tests/
    ├── test_products.py
    ├── test_authentication.py
    └── test_performance.py
```

---

## Evaluation Criteria

### 1. ✅ Functionality

- [x] CRUD APIs fully functional for products, categories, and users
- [x] User authentication with JWT implementation
- [x] Filtering logic working correctly (by category, price, attributes)
- [x] Sorting functionality across multiple fields
- [x] Pagination implemented and tested
- [x] Review and rating system operational
- [x] All endpoints return appropriate status codes and error messages

### 2. ✅ Code Quality

- [x] Clean, readable, and maintainable code
- [x] Proper separation of concerns (models, views, serializers)
- [x] Consistent naming conventions throughout
- [x] Comprehensive docstrings and comments
- [x] DRY principle followed (no code duplication)
- [x] Strategic database indexing for high-performance queries
- [x] Input validation on all endpoints
- [x] Proper error handling and logging

### 3. ✅ User Experience

- [x] Comprehensive API documentation (Swagger/OpenAPI)
- [x] Clear error messages and status codes
- [x] Consistent API response format
- [x] Secure authentication without exposure of credentials
- [x] Fast response times due to optimization
- [x] Easy frontend integration with clear endpoints

### 4. ✅ Version Control

- [x] Frequent and descriptive commit messages
- [x] Logical commit history showing progression
- [x] Well-organized repository structure
- [x] `.gitignore` properly configured
- [x] Clear README with setup instructions
- [x] Branching strategy (if applicable)

---

## Performance Benchmarks

Target performance metrics:

| Metric                          | Target  |
| ------------------------------- | ------- |
| List Products (1000+ items)     | < 200ms |
| Filter Products                 | < 300ms |
| Get Product Details             | < 100ms |
| Create Product                  | < 150ms |
| Authentication (Login/Register) | < 200ms |
| Database Query Response         | < 50ms  |
| API Response Time (p95)         | < 500ms |

---

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip and virtualenv

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd ecommerce-backend

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Access API at http://localhost:8000/api/
# Access Swagger docs at http://localhost:8000/api/docs/
```

---

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_products.py

# Run specific test
pytest tests/test_products.py::test_list_products
```

---

## Next Steps

1. **Expand to Related Services**: Add order management, payment processing
2. **Implement Caching**: Add Redis for product caching
3. **Search Optimization**: Implement Elasticsearch for advanced search
4. **Real-time Features**: Add WebSockets for real-time notifications
5. **Analytics**: Implement product analytics and user behavior tracking
6. **Recommendation System**: Add ML-based product recommendations

---

## Resources & References

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [JWT Authentication](https://jwt.io/)
- [RESTful API Best Practices](https://restfulapi.net/)
- [DRF Spectacular](https://drf-spectacular.readthedocs.io/)

---

## License

This project is part of the ProDev Backend Engineering program and follows the program's license terms.

---

**Last Updated**: January 2026  
**Status**: Active Development  
**Contributors**: ProDev Backend Engineering Learners
