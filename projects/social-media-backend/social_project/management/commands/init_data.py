"""
Management command to initialize sample data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from posts.models import Post, Comment
from interactions.models import PostLike, Share
from users.models import Follow


class Command(BaseCommand):
    help = 'Initialize sample data for the social media backend'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data initialization...'))

        # Create sample users
        self.stdout.write('Creating sample users...')
        users = []
        for i in range(5):
            user, created = User.objects.get_or_create(
                username=f'user{i+1}',
                defaults={
                    'email': f'user{i+1}@example.com',
                    'first_name': f'User {i+1}',
                    'last_name': 'Test'
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

        # Create sample posts
        self.stdout.write('Creating sample posts...')
        posts = []
        sample_posts = [
            ('Django Tips and Tricks', 'Learn some advanced Django techniques for building scalable applications.'),
            ('GraphQL Best Practices', 'Explore best practices when using GraphQL in your projects.'),
            ('PostgreSQL Performance Tuning', 'Tips for optimizing PostgreSQL query performance.'),
            ('Building Real-time APIs', 'Learn how to build real-time APIs using WebSockets and GraphQL subscriptions.'),
            ('Scaling Social Media Platforms', 'Challenges and solutions for scaling to millions of users.'),
        ]

        for i, (title, content) in enumerate(sample_posts):
            post, created = Post.objects.get_or_create(
                title=title,
                defaults={
                    'author': users[i % len(users)],
                    'content': content,
                    'is_published': True
                }
            )
            if created:
                posts.append(post)

        # Create sample comments
        self.stdout.write('Creating sample comments...')
        if posts:
            for i, post in enumerate(posts[:3]):
                Comment.objects.get_or_create(
                    post=post,
                    author=users[(i + 1) % len(users)],
                    defaults={
                        'content': f'Great post! This is very helpful. Thanks for sharing.',
                    }
                )

        # Create sample likes
        self.stdout.write('Creating sample likes...')
        for post in posts[:3]:
            for user in users[1:3]:
                PostLike.objects.get_or_create(post=post, user=user)

        # Create sample follows
        self.stdout.write('Creating sample follows...')
        for i in range(len(users) - 1):
            Follow.objects.get_or_create(
                follower=users[i],
                following=users[i + 1]
            )

        self.stdout.write(self.style.SUCCESS('Data initialization completed successfully!'))
        self.stdout.write(self.style.WARNING(f'Created {len(users)} users'))
        self.stdout.write(self.style.WARNING(f'Created {len(posts)} posts'))
