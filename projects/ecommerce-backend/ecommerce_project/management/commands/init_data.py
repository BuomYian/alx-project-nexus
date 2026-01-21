"""
Django management command to initialize the project with sample data
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from categories.models import Category
from products.models import Product, ProductAttribute
from reviews.models import Review
from decimal import Decimal

User = get_user_model()


class Command(BaseCommand):
    help = 'Initialize the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('🚀 Initializing E-Commerce Backend...')
        
        # Create admin user
        self.create_admin_user()
        
        # Create sample users
        self.create_sample_users()
        
        # Create categories
        self.create_categories()
        
        # Create products
        self.create_products()
        
        # Create reviews
        self.create_reviews()
        
        self.stdout.write(self.style.SUCCESS('✅ Initialization complete!'))

    def create_admin_user(self):
        """Create admin superuser"""
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@ecommerce.com',
                password='admin123'
            )
            self.stdout.write('✓ Created admin user (admin/admin123)')

    def create_sample_users(self):
        """Create sample users"""
        users = [
            {'username': 'john', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'bob', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Johnson'},
        ]
        
        for user_data in users:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password='testpass123',
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )
        self.stdout.write('✓ Created sample users')

    def create_categories(self):
        """Create sample categories"""
        categories_data = [
            {'name': 'Electronics', 'description': 'Electronic devices and gadgets'},
            {'name': 'Clothing', 'description': 'Apparel and fashion items'},
            {'name': 'Books', 'description': 'Physical and digital books'},
            {'name': 'Home & Kitchen', 'description': 'Home and kitchen appliances'},
            {'name': 'Sports', 'description': 'Sports equipment and accessories'},
        ]
        
        for cat_data in categories_data:
            if not Category.objects.filter(name=cat_data['name']).exists():
                Category.objects.create(**cat_data)
        
        self.stdout.write('✓ Created categories')

    def create_products(self):
        """Create sample products"""
        admin = User.objects.get(username='admin')
        electronics = Category.objects.get(name='Electronics')
        clothing = Category.objects.get(name='Clothing')
        books = Category.objects.get(name='Books')
        
        products_data = [
            {
                'name': 'Wireless Headphones',
                'description': 'Premium wireless headphones with noise cancellation',
                'short_description': 'High-quality wireless headphones',
                'sku': 'HEAD-001',
                'price': Decimal('199.99'),
                'discount_price': Decimal('149.99'),
                'quantity_in_stock': 50,
                'category': electronics,
                'image': 'products/headphones.jpg',
                'attributes': [
                    {'attribute_key': 'Color', 'attribute_value': 'Black'},
                    {'attribute_key': 'Warranty', 'attribute_value': '2 Years'}
                ]
            },
            {
                'name': 'Laptop Computer',
                'description': 'High-performance laptop for professionals',
                'short_description': 'Powerful laptop with SSD',
                'sku': 'LAPTOP-001',
                'price': Decimal('1299.99'),
                'discount_price': None,
                'quantity_in_stock': 20,
                'category': electronics,
                'image': 'products/laptop.jpg',
                'attributes': [
                    {'attribute_key': 'Processor', 'attribute_value': 'Intel i7'},
                    {'attribute_key': 'RAM', 'attribute_value': '16GB'}
                ]
            },
            {
                'name': 'T-Shirt',
                'description': 'Comfortable cotton t-shirt',
                'short_description': 'Classic cotton t-shirt',
                'sku': 'TSHIRT-001',
                'price': Decimal('29.99'),
                'discount_price': Decimal('19.99'),
                'quantity_in_stock': 100,
                'category': clothing,
                'image': 'products/tshirt.jpg',
                'attributes': [
                    {'attribute_key': 'Color', 'attribute_value': 'Blue'},
                    {'attribute_key': 'Size', 'attribute_value': 'M'}
                ]
            },
            {
                'name': 'Python Programming',
                'description': 'Learn Python programming from scratch',
                'short_description': 'Beginner-friendly Python book',
                'sku': 'BOOK-001',
                'price': Decimal('49.99'),
                'discount_price': None,
                'quantity_in_stock': 30,
                'category': books,
                'image': 'products/python_book.jpg',
                'attributes': [
                    {'attribute_key': 'Author', 'attribute_value': 'John Smith'},
                    {'attribute_key': 'Pages', 'attribute_value': '450'}
                ]
            },
        ]
        
        for prod_data in products_data:
            if not Product.objects.filter(sku=prod_data['sku']).exists():
                attributes_data = prod_data.pop('attributes', [])
                product = Product.objects.create(
                    **prod_data,
                    created_by=admin
                )
                
                # Add attributes
                for attr_data in attributes_data:
                    ProductAttribute.objects.create(product=product, **attr_data)
        
        self.stdout.write('✓ Created sample products')

    def create_reviews(self):
        """Create sample reviews"""
        users = User.objects.filter(username__in=['john', 'jane', 'bob'])
        products = Product.objects.all()[:3]
        
        reviews_data = [
            {'rating': 5, 'title': 'Excellent product!', 'comment': 'Great quality and fast delivery. Highly recommended!'},
            {'rating': 4, 'title': 'Very good', 'comment': 'Good product but could be better in some aspects.'},
            {'rating': 3, 'title': 'Average', 'comment': 'It\'s okay, does what it\'s supposed to do.'},
        ]
        
        for product in products:
            for user in users:
                if not Review.objects.filter(product=product, user=user).exists():
                    review_data = reviews_data[0]
                    Review.objects.create(
                        product=product,
                        user=user,
                        rating=review_data['rating'],
                        title=review_data['title'],
                        comment=review_data['comment'],
                        is_verified_purchase=True
                    )
                    reviews_data = reviews_data[1:] + [reviews_data[0]]
        
        self.stdout.write('✓ Created sample reviews')
