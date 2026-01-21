# PostgreSQL Setup Guide

## Overview

Your E-Commerce Backend has been configured to use **PostgreSQL** instead of SQLite. This provides better performance and is recommended for production environments.

## PostgreSQL Configuration

**Current settings in `.env`:**
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=ecommerce_password
DB_HOST=localhost
DB_PORT=5432
```

## Installation & Setup

### Linux (Ubuntu/Debian)

```bash
# Install PostgreSQL
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start PostgreSQL service
sudo systemctl start postgresql
sudo systemctl enable postgresql

# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL shell, create database and user:
CREATE DATABASE ecommerce_db;
CREATE USER ecommerce_user WITH PASSWORD 'ecommerce_password';
ALTER ROLE ecommerce_user SET client_encoding TO 'utf8';
ALTER ROLE ecommerce_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE ecommerce_user SET default_transaction_deferrable TO on;
ALTER ROLE ecommerce_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE ecommerce_db TO ecommerce_user;
\q
```

### macOS (with Homebrew)

```bash
# Install PostgreSQL
brew install postgresql@15

# Start PostgreSQL
brew services start postgresql@15

# Create database and user
createuser -P ecommerce_user  # Enter password: ecommerce_password
createdb -O ecommerce_user ecommerce_db
```

### Windows

1. Download PostgreSQL from [postgresql.org](https://www.postgresql.org/download/windows/)
2. Run installer and remember the password you set for `postgres` user
3. Open pgAdmin (included with PostgreSQL)
4. Create a new database:
   - Database name: `ecommerce_db`
   - Owner: Create new user `ecommerce_user` with password `ecommerce_password`

### Docker (Recommended)

Run PostgreSQL in a container:

```bash
docker run --name ecommerce-postgres \
  -e POSTGRES_DB=ecommerce_db \
  -e POSTGRES_USER=ecommerce_user \
  -e POSTGRES_PASSWORD=ecommerce_password \
  -p 5432:5432 \
  -d postgres:15
```

## Verify PostgreSQL Connection

Test the connection:

```bash
psql -U ecommerce_user -d ecommerce_db -h localhost -W
# Enter password: ecommerce_password
# If successful, you'll see: ecommerce_db=>
# Type: \q to exit
```

## Install PostgreSQL Python Adapter

The `psycopg2-binary` package is already in your requirements.txt, but verify it's installed:

```bash
cd projects/ecommerce-backend
source venv/bin/activate
pip list | grep psycopg2
```

If not installed:
```bash
pip install psycopg2-binary==2.9.9
```

## Django Setup with PostgreSQL

### 1. Verify .env Configuration

Check your `.env` file has PostgreSQL settings:
```bash
cat .env | grep DB_
```

Expected output:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
DB_PASSWORD=ecommerce_password
DB_HOST=localhost
DB_PORT=5432
```

### 2. Run Migrations

```bash
cd projects/ecommerce-backend
source venv/bin/activate

# Apply all migrations to PostgreSQL
python manage.py migrate
```

You should see:
```
Operations to perform:
  Apply all migrations: accounts, admin, auth, categories, contenttypes, products, reviews, sessions
Running migrations:
  Applying contenttypes.0001_initial... OK
  ...
```

### 3. Create Superuser

```bash
python manage.py createsuperuser
```

Or with automatic password:
```bash
python manage.py createsuperuser --username admin --email admin@example.com --noinput
python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); u = User.objects.get(username='admin'); u.set_password('admin123'); u.save()"
```

### 4. Start Development Server

```bash
python manage.py runserver
```

## Verify PostgreSQL is Running

### Check connection in Django shell:

```bash
python manage.py shell
```

Then in the Python shell:
```python
from django.db import connection
print(connection.get_connection_params())
# Should show your PostgreSQL connection details

# Test a query
from accounts.models import User
print(User.objects.count())
# Should return a number (or 0 if no users)
```

## Environment Variables

You can customize the PostgreSQL connection by editing `.env`:

| Variable | Default | Purpose |
|----------|---------|---------|
| `DB_ENGINE` | `django.db.backends.postgresql` | Database backend |
| `DB_NAME` | `ecommerce_db` | Database name |
| `DB_USER` | `ecommerce_user` | Database user |
| `DB_PASSWORD` | `ecommerce_password` | Database password |
| `DB_HOST` | `localhost` | Database host |
| `DB_PORT` | `5432` | Database port |

## Common Issues & Solutions

### Issue: "Connection refused"
**Solution**: Make sure PostgreSQL is running
```bash
# Linux
sudo systemctl status postgresql

# macOS
brew services list

# Docker
docker ps | grep postgres
```

### Issue: "FATAL: Ident authentication failed"
**Solution**: Check username and password in `.env` match your PostgreSQL setup

### Issue: "could not translate host name"
**Solution**: Verify `DB_HOST` is correct (usually `localhost` or `127.0.0.1`)

### Issue: "database does not exist"
**Solution**: Create the database manually (see Installation section above)

## Production Settings

For production, update `.env`:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_prod_db
DB_USER=your_prod_user
DB_PASSWORD=your_secure_password
DB_HOST=your.postgres.host.com
DB_PORT=5432
```

## Backup & Restore

### Backup PostgreSQL database:
```bash
pg_dump -U ecommerce_user -d ecommerce_db -h localhost > backup.sql
```

### Restore PostgreSQL database:
```bash
psql -U ecommerce_user -d ecommerce_db -h localhost < backup.sql
```

## Resources

- [PostgreSQL Official Docs](https://www.postgresql.org/docs/)
- [Django PostgreSQL Documentation](https://docs.djangoproject.com/en/4.2/ref/databases/#postgresql-notes)
- [psycopg2 Documentation](https://www.psycopg.org/)

---

**Your E-Commerce Backend is now configured for PostgreSQL!** 🚀

Run `python manage.py migrate` to create all tables in PostgreSQL.
