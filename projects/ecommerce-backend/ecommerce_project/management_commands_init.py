"""
Django management command to initialize the project
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from categories.models import Category
from products.models import Product


User = get_user_model()


class Command(BaseCommand):
    help = 'Initialize the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating superuser...')

        # Create superuser
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ecommerce.com',
                password='admin123'
            )
            self.stdout.write(self.style.SUCCESS(
                'Superuser created: admin/admin123'))
        else:
            self.stdout.write('Superuser already exists')

        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Apparel and fashion items'},
            {'name': 'Books', 'description': 'Physical and digital books'},
            {'name': 'Home & Kitchen', 'description': 'Home and kitchen appliances'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
        ]

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')

        self.stdout.write(self.style.SUCCESS('Initialization complete!'))
