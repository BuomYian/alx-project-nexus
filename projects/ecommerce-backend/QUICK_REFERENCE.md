# E-Commerce Backend - Quick Reference Guide

## 🚀 Getting Started (5 Minutes)

### Step 1: Navigate to Project
```bash
cd projects/ecommerce-backend
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Setup Database
```bash
# Copy environment file
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Initialize sample data (optional)
python manage.py init_data
```

### Step 5: Run Development Server
```bash
python manage.py runserver
```

**Server Running! 🎉**
- API: http://localhost:8000/api/
- Swagger Docs: http://localhost:8000/api/docs/
- Admin: http://localhost:8000/admin/

---

## 📚 API Endpoints Quick Reference

### Authentication
```
POST   /api/auth/register/          # Register new user
POST   /api/auth/login/             # Login and get tokens
POST   /api/auth/refresh/           # Refresh access token
GET    /api/auth/users/me/          # Get current user profile
PUT    /api/auth/users/update_profile/  # Update profile
POST   /api/auth/users/change_password/ # Change password
```

### Products
```
GET    /api/products/               # List all products
POST   /api/products/               # Create product
GET    /api/products/{id}/          # Get product details
PUT    /api/products/{id}/          # Update product
DELETE /api/products/{id}/          # Delete product
GET    /api/products/featured/      # Get featured products
GET    /api/products/best_sellers/  # Get best sellers
GET    /api/products/top_rated/     # Get top rated
GET    /api/products/latest/        # Get latest products
```

### Categories
```
GET    /api/categories/             # List all categories
POST   /api/categories/             # Create category
GET    /api/categories/{id}/        # Get category details
PUT    /api/categories/{id}/        # Update category
DELETE /api/categories/{id}/        # Delete category
```

### Reviews
```
GET    /api/reviews/                # List all reviews
POST   /api/reviews/                # Create review
GET    /api/reviews/{id}/           # Get review details
PUT    /api/reviews/{id}/           # Update review
DELETE /api/reviews/{id}/           # Delete review
POST   /api/reviews/{id}/mark_helpful/      # Mark as helpful
POST   /api/reviews/{id}/mark_unhelpful/    # Mark as unhelpful
```

---

## 🔍 Filtering & Sorting Examples

### Filter by Price Range
```bash
curl "http://localhost:8000/api/products/?min_price=100&max_price=500"
```

### Filter by Category
```bash
curl "http://localhost:8000/api/products/?category=1"
```

### Search Products
```bash
curl "http://localhost:8000/api/products/?search=laptop"
```

### Sort by Price (Descending)
```bash
curl "http://localhost:8000/api/products/?ordering=-price"
```

### Paginate Results
```bash
curl "http://localhost:8000/api/products/?page=1&page_size=20"
```

### Combined Example
```bash
curl "http://localhost:8000/api/products/?category=1&min_price=50&max_price=500&ordering=-price&page=1&page_size=10"
```

---

## 🔐 Authentication Flow

### 1. Register New User
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john",
    "email": "john@example.com",
    "password": "StrongPass123",
    "password2": "StrongPass123"
  }'
```

### 2. Login to Get Tokens
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "StrongPass123"
  }'

# Response includes:
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
# }
```

### 3. Use Access Token in Requests
```bash
curl http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 4. Refresh Token When Expired
```bash
curl -X POST http://localhost:8000/api/auth/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

---

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test File
```bash
pytest tests/test_products.py
```

### Run with Coverage Report
```bash
pytest --cov=. --cov-report=html
```

### Run in Verbose Mode
```bash
pytest -v
```

### Run Specific Test
```bash
pytest tests/test_products.py::TestProductAPI::test_list_products
```

---

## 📦 Project Structure

```
ecommerce-backend/
├── manage.py                  # Django management script
├── requirements.txt           # Project dependencies
├── .env.example              # Environment variables template
├── SETUP.md                  # Detailed setup guide
├── README.md                 # Project overview
├── API_SPECIFICATION.md      # Complete API docs
├── IMPLEMENTATION_GUIDE.md   # Code examples
├── QUICK_REFERENCE.md        # This file
├── Dockerfile                # Docker configuration
├── docker-compose.yml        # Docker compose config
├── ecommerce_project/        # Main project folder
│   ├── settings.py           # Django settings
│   ├── urls.py              # Main URL routing
│   ├── wsgi.py              # WSGI configuration
│   ├── pagination.py        # Custom pagination
│   └── management/          # Management commands
│       └── commands/
│           └── init_data.py # Initialize sample data
├── accounts/                # User authentication
│   ├── models.py            # User model
│   ├── serializers.py       # User serializers
│   ├── views.py             # User views
│   ├── urls.py              # Auth URLs
│   └── admin.py             # Admin configuration
├── products/                # Product management
│   ├── models.py            # Product models
│   ├── serializers.py       # Product serializers
│   ├── views.py             # Product views
│   ├── filters.py           # Product filters
│   ├── urls.py              # Product URLs
│   └── admin.py             # Admin configuration
├── categories/              # Category management
│   ├── models.py            # Category model
│   ├── serializers.py       # Category serializers
│   ├── views.py             # Category views
│   ├── urls.py              # Category URLs
│   └── admin.py             # Admin configuration
├── reviews/                 # Review management
│   ├── models.py            # Review model
│   ├── serializers.py       # Review serializers
│   ├── views.py             # Review views
│   ├── urls.py              # Review URLs
│   └── admin.py             # Admin configuration
└── tests/                   # Test suite
    ├── test_products.py     # Product tests
    ├── test_auth.py         # Auth tests
    └── conftest.py          # Pytest configuration
```

---

## 🛠️ Common Commands

### Create Superuser
```bash
python manage.py createsuperuser
```

### Initialize Sample Data
```bash
python manage.py init_data
```

### Run Migrations
```bash
python manage.py migrate
```

### Create Migrations
```bash
python manage.py makemigrations
```

### Access Django Shell
```bash
python manage.py shell
```

### Collect Static Files
```bash
python manage.py collectstatic
```

### Check Project Status
```bash
python manage.py check
```

---

## 🐛 Troubleshooting

### Module Not Found Error
```bash
# Activate virtual environment
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt
```

### Port 8000 Already in Use
```bash
# Run on different port
python manage.py runserver 8001

# Or kill process on port 8000
lsof -i :8000
kill -9 <PID>
```

### Database Errors
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading
```bash
# Collect static files
python manage.py collectstatic --noinput
```

---

## 📖 Documentation References

- **[Full Setup Guide](./SETUP.md)** - Detailed setup instructions
- **[API Specification](./API_SPECIFICATION.md)** - Complete API documentation
- **[Implementation Guide](./IMPLEMENTATION_GUIDE.md)** - Code examples and implementation details
- **[Project README](./README.md)** - Project overview and features

---

## 🎯 Key Features Implemented

✅ **User Authentication**
- User registration and login
- JWT token-based authentication
- Token refresh and blacklisting
- Password change functionality

✅ **Product Management**
- Complete CRUD operations
- Product filtering by category, price, attributes
- Advanced sorting capabilities
- Product attributes support
- Featured and best-seller listings

✅ **Category Management**
- Category CRUD operations
- Hierarchical category support
- Product count tracking

✅ **Review System**
- User reviews and ratings
- Helpful/unhelpful voting
- Review filtering by rating
- Verified purchase support

✅ **API Documentation**
- Swagger/OpenAPI integration
- ReDoc documentation
- Interactive API testing

✅ **Advanced Features**
- Custom pagination
- Advanced filtering
- Sorting on multiple fields
- Search functionality
- Rate limiting
- CORS support
- Comprehensive logging

---

## 🚀 Deployment Checklist

- [ ] Update `.env` with production values
- [ ] Set `DEBUG = False`
- [ ] Change `SECRET_KEY`
- [ ] Configure allowed hosts
- [ ] Set up PostgreSQL database
- [ ] Run migrations on production
- [ ] Collect static files
- [ ] Set up SSL/HTTPS
- [ ] Configure email backend
- [ ] Set up monitoring and logging
- [ ] Test all endpoints
- [ ] Deploy with gunicorn or similar

---

## 📞 Support

For questions or issues:
1. Check the [Setup Guide](./SETUP.md)
2. Review [API Specification](./API_SPECIFICATION.md)
3. Look at [Implementation Guide](./IMPLEMENTATION_GUIDE.md)
4. Check test files for usage examples
5. Review Django REST Framework documentation

---

**Happy Developing! 🎉**

Last Updated: January 2026  
Version: 1.0.0
