# E-Commerce Backend - Setup & Installation Guide

## Quick Start

### Option 1: Local Development (SQLite)

```bash
# 1. Navigate to project directory
cd projects/ecommerce-backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file
cp .env.example .env

# 5. Run migrations
python manage.py migrate

# 6. Create superuser
python manage.py createsuperuser

# 7. Run development server
python manage.py runserver

# API will be available at:
# - Main API: http://localhost:8000/api/
# - Swagger Docs: http://localhost:8000/api/docs/
# - ReDoc: http://localhost:8000/api/redoc/
# - Admin: http://localhost:8000/admin/
```

### Option 2: Docker Compose (PostgreSQL)

```bash
# 1. Make sure Docker and Docker Compose are installed

# 2. Navigate to project directory
cd projects/ecommerce-backend

# 3. Build and run containers
docker-compose up -d

# 4. Create superuser (if not auto-created)
docker-compose exec web python manage.py createsuperuser

# 5. Initialize sample data
docker-compose exec web python manage.py init_data

# API will be available at:
# - http://localhost:8000/api/
# - http://localhost:8000/api/docs/
```

---

## Configuration

### Database Setup

#### Using SQLite (Development)
Edit `.env`:
```
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

#### Using PostgreSQL
Install PostgreSQL and create database:
```bash
createdb ecommerce_db
```

Edit `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

---

## Common Commands

### Database Operations
```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Initialize sample data
python manage.py shell < scripts/init_data.py
```

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_products.py

# Run specific test
pytest tests/test_products.py::TestProductAPI::test_list_products

# Run tests with verbose output
pytest -v

# Run tests in parallel
pytest -n auto
```

### Code Quality
```bash
# Format code with Black
black .

# Check code style
flake8 .

# Sort imports
isort .

# Run all checks
black . && flake8 . && isort .
```

### API Documentation
```bash
# Generate OpenAPI schema
python manage.py spectacular --file schema.yml

# The schema is automatically available at:
# - /api/schema/ (JSON)
# - /api/docs/ (Swagger UI)
# - /api/redoc/ (ReDoc)
```

---

## API Testing

### Using cURL

#### Registration
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "SecurePass123",
    "password2": "SecurePass123"
  }'
```

#### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123"
  }'
```

#### List Products
```bash
curl http://localhost:8000/api/products/
```

#### List Products with Filters
```bash
curl "http://localhost:8000/api/products/?category=1&min_price=100&max_price=500&ordering=-price"
```

#### Create Product (Authenticated)
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Laptop",
    "description": "High-performance laptop",
    "sku": "LAPTOP-001",
    "price": "999.99",
    "quantity_in_stock": 10,
    "category": 1,
    "image": "laptop.jpg"
  }'
```

### Using Postman

1. Import the [Postman Collection](./postman_collection.json)
2. Set environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: Your JWT token from login
3. Use pre-configured requests for all endpoints

---

## Deployment

### Production Checklist

```bash
# 1. Update .env for production
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-very-secret-key

# 2. Collect static files
python manage.py collectstatic --noinput

# 3. Run migrations
python manage.py migrate --noinput

# 4. Run server with gunicorn
gunicorn ecommerce_project.wsgi:application --workers 4 --bind 0.0.0.0:8000
```

### Deploying to Heroku

```bash
# 1. Create Heroku app
heroku create your-app-name

# 2. Add PostgreSQL addon
heroku addons:create heroku-postgresql:standard-0 --app your-app-name

# 3. Set environment variables
heroku config:set DEBUG=False --app your-app-name
heroku config:set SECRET_KEY=your-secret-key --app your-app-name

# 4. Deploy
git push heroku main

# 5. Run migrations
heroku run python manage.py migrate --app your-app-name

# 6. Create superuser
heroku run python manage.py createsuperuser --app your-app-name
```

---

## Troubleshooting

### Port Already in Use
```bash
# Kill process on port 8000
lsof -i :8000
kill -9 <PID>

# Or run on different port
python manage.py runserver 8001
```

### Database Migration Issues
```bash
# Reset migrations (development only)
python manage.py migrate --fake accounts zero
python manage.py migrate

# Or start fresh
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Permission Denied Errors
```bash
# On Mac/Linux, make manage.py executable
chmod +x manage.py

# Or always run with python
python manage.py <command>
```

### Module Not Found
```bash
# Ensure virtual environment is activated
source venv/bin/activate

# Reinstall requirements
pip install -r requirements.txt --force-reinstall
```

---

## Project Structure

```
ecommerce-backend/
├── ecommerce_project/     # Main project settings
│   ├── settings.py        # Django settings
│   ├── urls.py           # Main URL configuration
│   ├── wsgi.py           # WSGI application
│   └── pagination.py     # Custom pagination
├── accounts/             # User authentication app
│   ├── models.py         # User model
│   ├── serializers.py    # User serializers
│   ├── views.py          # User viewsets
│   ├── urls.py           # Auth URLs
│   └── admin.py          # Admin configuration
├── products/             # Products app
│   ├── models.py         # Product and attribute models
│   ├── serializers.py    # Product serializers
│   ├── views.py          # Product viewsets
│   ├── filters.py        # Product filters
│   ├── urls.py           # Product URLs
│   └── admin.py          # Admin configuration
├── categories/           # Categories app
│   ├── models.py         # Category model
│   ├── serializers.py    # Category serializers
│   ├── views.py          # Category viewsets
│   ├── urls.py           # Category URLs
│   └── admin.py          # Admin configuration
├── reviews/              # Reviews app
│   ├── models.py         # Review model
│   ├── serializers.py    # Review serializers
│   ├── views.py          # Review viewsets
│   ├── urls.py           # Review URLs
│   └── admin.py          # Admin configuration
├── tests/                # Test suite
│   ├── test_products.py  # Product tests
│   ├── test_auth.py      # Authentication tests
│   └── conftest.py       # Pytest configuration
├── manage.py             # Django management
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── docker-compose.yml    # Docker compose configuration
├── Dockerfile            # Docker configuration
└── README.md            # Project documentation
```

---

## Next Steps

1. **Create Sample Data**: Run management commands to populate initial data
2. **Write More Tests**: Expand test coverage for all endpoints
3. **Add Caching**: Implement Redis for performance optimization
4. **Set up CI/CD**: Configure GitHub Actions or similar
5. **Monitor Performance**: Add monitoring and logging
6. **Security Hardening**: Review security settings for production

---

## Support & Documentation

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Swagger/OpenAPI](https://swagger.io/)

---

**Happy Coding! 🚀**
