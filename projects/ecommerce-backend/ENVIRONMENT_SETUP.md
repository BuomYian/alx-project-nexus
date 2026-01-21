# Environment Setup Guide

This guide walks you through setting up your development environment for the E-Commerce Backend project.

## Prerequisites

- Python 3.10+ (verify with `python3 --version`)
- pip (Python package manager)
- git (for version control)
- A terminal/command line interface

## Setup Steps

### 1. Navigate to Project Directory

```bash
cd projects/ecommerce-backend
```

### 2. Create Virtual Environment (Recommended)

#### Option A: Using venv (Built-in)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Option B: Using conda
```bash
conda create -n ecommerce python=3.10
conda activate ecommerce
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected Output:** All 31 packages installed successfully (including Django 4.2.7, DRF 3.14.0, JWT 5.3.1, etc.)

### 4. Create Logs Directory

The Django logging configuration requires a logs directory:

```bash
mkdir -p logs
```

### 5. Environment Configuration

Create a `.env` file from the template:

```bash
cp .env.example .env
```

**Key environment variables:**
- `DEBUG=True` (for development)
- `ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0`
- `DATABASE_URL=sqlite:///db.sqlite3` (development)
- `SECRET_KEY=your-secret-key-here`
- `JWT_SECRET=your-jwt-secret-here`

### 6. Run Database Migrations

```bash
python manage.py migrate
```

**Expected Output:**
```
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying admin.0001_initial... OK
  ...
```

### 7. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

**You'll be prompted to enter:**
- Username: `admin`
- Email: `admin@example.com`
- Password: (enter twice)

**For quick testing**, use these credentials:
```
Username: admin
Email: admin@localhost.com
Password: admin123
```

### 8. Verify Installation

Check that everything is working:

```bash
python manage.py check
```

**Expected Output:**
```
System check identified no issues (0 silenced).
```

### 9. Start Development Server

```bash
python manage.py runserver
```

**Expected Output:**
```
January 21, 2026 - 10:52:31
Django version 4.2.7, using settings 'ecommerce_project.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Access the Application

Once the server is running, open your browser and navigate to:

### API Documentation
- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/
- **OpenAPI Schema**: http://127.0.0.1:8000/api/schema/

### Admin Interface
- **URL**: http://127.0.0.1:8000/admin/
- **Login**: Use the superuser credentials created above

### API Endpoints
- **Products**: http://127.0.0.1:8000/api/products/
- **Categories**: http://127.0.0.1:8000/api/categories/
- **Reviews**: http://127.0.0.1:8000/api/reviews/
- **Auth**: http://127.0.0.1:8000/api/auth/

## Load Sample Data (Optional)

To populate the database with sample data:

```bash
python manage.py init_data
```

This creates:
- 1 admin user
- 3 regular users
- 5 product categories
- 4 sample products
- Multiple reviews

## Running Tests

Run the test suite with pytest:

```bash
pytest
```

**Run with coverage:**
```bash
pytest --cov=. --cov-report=html
```

**Run specific tests:**
```bash
pytest tests/test_auth.py
pytest tests/test_products.py::test_list_products
```

## Development Tools

### Code Formatting (Black)
```bash
black .
```

### Code Linting (Flake8)
```bash
flake8 .
```

### Import Sorting (isort)
```bash
isort .
```

### Full Code Quality Check
```bash
black . && flake8 . && isort .
```

## Docker Setup (Optional)

If you prefer to run with Docker:

### Build and Start Containers
```bash
docker-compose up -d
```

### View Logs
```bash
docker-compose logs -f web
```

### Run Migrations in Container
```bash
docker-compose exec web python manage.py migrate
```

### Stop Containers
```bash
docker-compose down
```

## Troubleshooting

### Issue: "No module named 'django'"
**Solution**: Ensure virtual environment is activated and dependencies are installed
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Issue: "No such file or directory: logs/django.log"
**Solution**: Create the logs directory
```bash
mkdir -p logs
```

### Issue: "ModuleNotFoundError: No module named 'psycopg2'"
**Solution**: Install psycopg2-binary (included in requirements)
```bash
pip install psycopg2-binary==2.9.9
```

### Issue: "Database migration errors"
**Solution**: Reset the database
```bash
rm db.sqlite3
python manage.py migrate
```

### Issue: Port 8000 already in use
**Solution**: Run on a different port
```bash
python manage.py runserver 8001
```

### Issue: "SECRET_KEY not set"
**Solution**: Ensure .env file exists with SECRET_KEY
```bash
cp .env.example .env
# Edit .env and add/verify SECRET_KEY
```

## Next Steps

After successful setup:

1. **Read Documentation**
   - [API_SPECIFICATION.md](API_SPECIFICATION.md) - Complete endpoint documentation
   - [IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md) - Code architecture and examples
   - [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Common commands and workflows

2. **Test the API**
   - Visit http://127.0.0.1:8000/api/docs/ for interactive API testing
   - Try registering a new user
   - Browse products and post reviews

3. **Explore the Code**
   - Start with `accounts/` for authentication patterns
   - Review `products/` for advanced filtering and pagination
   - Check `reviews/` for complex model relationships

4. **Run Tests**
   - Execute `pytest` to verify everything works
   - Review test files in `tests/` directory

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| `DEBUG` | `True` | Enable debug mode |
| `ALLOWED_HOSTS` | `localhost,127.0.0.1` | Allowed request hosts |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Database connection string |
| `SECRET_KEY` | `change-me` | Django secret key |
| `JWT_SECRET` | `jwt-secret-key` | JWT signing key |
| `CORS_ALLOWED_ORIGINS` | `localhost:3000,localhost:8000` | CORS allowed origins |
| `PAGINATION_PAGE_SIZE` | `20` | Default page size |
| `REST_FRAMEWORK_THROTTLE_RATES` | `100/hour` | Rate limiting |

## Quick Commands Cheat Sheet

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load sample data
python manage.py init_data

# Run development server
python manage.py runserver

# Run tests
pytest

# Run tests with coverage
pytest --cov=.

# Code formatting
black .

# Code linting
flake8 .

# Import sorting
isort .

# Django shell
python manage.py shell

# Database shell
python manage.py dbshell
```

## Support & Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django REST Framework**: https://www.django-rest-framework.org/
- **JWT Documentation**: https://django-rest-framework-simplejwt.readthedocs.io/
- **Project Issues**: Report issues on GitHub
- **Documentation**: See [00_START_HERE.md](00_START_HERE.md) for project overview

---

**Last Updated**: January 21, 2026
**Status**: ✅ Environment setup verified and working
