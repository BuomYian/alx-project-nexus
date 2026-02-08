FROM python:3.11-alpine

WORKDIR /app

# Install dependencies
RUN apk add --no-cache \
    postgresql-client \
    postgresql-dev \
    build-base \
    gcc \
    musl-dev

# Copy requirements from ecommerce-backend
COPY ecommerce-backend/requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire ecommerce-backend project
COPY ecommerce-backend/ .

# Create necessary directories
RUN mkdir -p logs media staticfiles

# Collect static files
RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["sh", "-c", "gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4"]
