# Blog Platform API

A RESTful API for a blogging platform built with Django REST Framework. This API allows users to create, read, update, and delete blog posts and comments.

## Features

- RESTful API for blog posts and comments
- Comprehensive test suite
- API documentation with Swagger/OpenAPI
- Docker support for easy setup and deployment

## Requirements

- Docker and Docker Compose (recommended)
- Python 3.11+
- Django 5.1.8
- Django REST Framework 3.15.0
- PostgreSQL

## Project Structure

```
│
├── manage.py
├── requirements.txt
├── .env
├── .gitignore
│
├── config/                     # Project settings
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py             # Base settings
│   │   ├── development.py      # Dev-specific settings
│   │   ├── production.py       # Prod-specific settings
│   ├── urls.py
│   ├── wsgi.py
│
├── apps/                       # All Django apps live here
│   ├── __init__.py
│   ├── core/                   # Core/shared utilities
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   ├── urls.py
│   │   ├── services.py         # Business logic
│   │   ├── selectors.py        # Read logic/queries
│   │   ├── permissions.py
│   │   ├── tests/
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py
│   │   │   ├── test_views.py
│
├── static/                     # Static files
├── media/                      # Media files (user uploads)
│
├── scripts/                    # Custom management/utility scripts
│
└── docker/                     # Docker config
    ├── Dockerfile
    └── docker-compose.yml
```

## Getting Started

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/yourusername/blog-platform-api.git
cd blog-platform-api
```

2. Create `.env` file from example:
```bash
cp .env.example .env
```

3. Build and run the Docker containers:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

4. Create database migrations:
```bash
docker-compose -f docker/docker-compose.yml exec web python manage.py makemigrations
docker-compose -f docker/docker-compose.yml exec web python manage.py migrate
```

5. Create a superuser (optional):
```bash
docker-compose -f docker/docker-compose.yml exec web python manage.py createsuperuser
```

### Without Docker

1. Clone the repository:
```bash
git clone https://github.com/yourusername/blog-platform-api.git
cd blog-platform-api
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file from example:
```bash
cp .env.example .env
```

4. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the development server:
```bash
python manage.py runserver
```

## API Documentation

Once the server is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/
- ReDoc: http://localhost:8000/redoc/

## API Endpoints

### Posts

- `POST /api/posts/`: Create a new blog post
- `GET /api/posts/`: List all blog posts
- `GET /api/posts/{id}/`: Get details of a specific post
- `PUT /api/posts/{id}/`: Update a post
- `DELETE /api/posts/{id}/`: Delete a post

### Comments

- `POST /api/posts/{post_id}/comments/`: Create a comment on a post
- `GET /api/posts/{post_id}/comments/`: List all comments for a post
- `GET /api/posts/{post_id}/comments/{id}/`: Get details of a specific comment
- `DELETE /api/posts/{post_id}/comments/{id}/`: Delete a comment

## Running Tests

```bash
# Using Docker
docker-compose -f docker/docker-compose.yml exec web python manage.py test

# Without Docker
python manage.py test
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 