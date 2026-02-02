# Social Media Feed Backend

A scalable GraphQL-based backend for managing posts, comments, and user interactions on a social media platform.

## Project Overview

This project demonstrates best practices for building high-traffic backend systems using:

- **Django** for robust backend development
- **PostgreSQL** for efficient relational data storage
- **GraphQL (Graphene)** for flexible and powerful API queries
- **GraphQL Playground** for intuitive API testing

## Key Features

### 1. GraphQL APIs

- Flexible querying of posts and interactions
- Resolvers for creating, fetching, and managing posts
- Support for nested queries and real-time interactions

### 2. Interaction Management

- Like posts and comments
- Create and manage comments
- Share posts with followers
- Track interaction analytics

### 3. High-Performance Queries

- Optimized database schema for high-volume operations
- Query optimization and caching
- Efficient pagination and filtering

### 4. API Testing

- GraphQL Playground for interactive testing
- Comprehensive query examples
- Real-time subscription support

## Tech Stack

- **Framework**: Django 4.2
- **Database**: PostgreSQL
- **GraphQL**: Graphene 3.3
- **API**: GraphQL Playground
- **Testing**: Pytest + Pytest-Django
- **Task Queue**: Celery + Redis

## Project Structure

```
social-media-backend/
├── requirements.txt
├── README.md
├── manage.py
├── pytest.ini
├── conftest.py
├── Dockerfile
├── docker-compose.yml
├── social_project/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│   └── schema.py
├── users/
│   ├── models.py
│   ├── views.py
│   └── serializers.py
├── posts/
│   ├── models.py
│   ├── views.py
│   ├── schema.py
│   └── serializers.py
├── interactions/
│   ├── models.py
│   ├── views.py
│   ├── schema.py
│   └── serializers.py
└── tests/
    ├── test_posts.py
    ├── test_interactions.py
    └── test_graphql.py
```

## Getting Started

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- Docker (optional)

### Installation

1. Clone the repository

```bash
git clone <repo-url>
cd social-media-backend
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

4. Set up environment variables

```bash
cp .env.example .env
# Edit .env with your PostgreSQL credentials
```

5. Run migrations

```bash
python manage.py migrate
```

6. Load initial data

```bash
python manage.py init_data
```

7. Start the development server

```bash
python manage.py runserver
```

Visit GraphQL Playground at: `http://localhost:8000/graphql/`

## API Documentation

### GraphQL Queries

#### Get all posts

```graphql
query {
  allPosts {
    id
    title
    content
    author {
      id
      username
    }
    createdAt
    likeCount
    commentCount
  }
}
```

#### Get post with interactions

```graphql
query {
  post(id: "1") {
    id
    title
    content
    comments {
      id
      content
      author {
        username
      }
    }
    likes {
      id
      user {
        username
      }
    }
  }
}
```

### GraphQL Mutations

#### Create a post

```graphql
mutation {
  createPost(title: "New Post", content: "Post content") {
    post {
      id
      title
      author {
        username
      }
    }
  }
}
```

#### Like a post

```graphql
mutation {
  likePost(postId: "1") {
    success
    message
  }
}
```

#### Add a comment

```graphql
mutation {
  createComment(postId: "1", content: "Great post!") {
    comment {
      id
      content
      author {
        username
      }
    }
  }
}
```

## Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=.
```

Run specific test file:

```bash
pytest tests/test_graphql.py -v
```

## Deployment

### Using Docker

1. Build the image

```bash
docker build -t social-media-backend .
```

2. Start with docker-compose

```bash
docker-compose up -d
```

### Production Deployment

- Use Gunicorn or uWSGI for WSGI
- Configure Nginx as reverse proxy
- Set up Redis for caching
- Use Celery for async tasks
- Enable SSL/TLS

## Performance Optimization

- Database query optimization with select_related and prefetch_related
- Caching with Redis
- Pagination for large datasets
- GraphQL query cost analysis
- Async tasks with Celery

## Contributing

1. Create a feature branch
2. Make changes and write tests
3. Commit with clear messages
4. Push to the branch
5. Create a pull request

## License

MIT License - See LICENSE file for details
