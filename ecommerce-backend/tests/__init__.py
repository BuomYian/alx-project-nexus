"""Initialize tests package"""

import pytest
import django
from django.conf import settings


def pytest_configure():
    """Configure pytest with Django settings"""
    if not settings.configured:
        settings.configure(
            DEBUG=True,
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
            INSTALLED_APPS=[
                'django.contrib.auth',
                'django.contrib.contenttypes',
                'rest_framework',
                'accounts',
                'products',
                'categories',
                'reviews',
            ]
        )
        django.setup()
