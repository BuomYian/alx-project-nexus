release: python manage.py migrate
web: gunicorn ecommerce_project.wsgi:application --bind 0.0.0.0:${PORT:-8000} --workers 4
