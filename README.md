# Blog Platform API

A RESTful API for a blogging platform built with Django REST Framework. This API allows users to create, read, update, and delete blog posts and comments, with additional features like categories, search, and like/dislike functionality.

## Features

- RESTful API for blog posts and comments
- Category system for organizing posts
- Like/dislike functionality for posts
- Search and filtering capabilities
- Pagination with 5 items per page
- Comprehensive test suite
- API documentation with Swagger/OpenAPI
- Docker support for easy setup and deployment

## Requirements

- Docker and Docker Compose (recommended)
- Python 3.11+
- Django 5.1.8
- Django REST Framework 3.15.0
- PostgreSQL 15
- django-filter 24.1

## Project Structure

```
│
├── manage.py
├── requirements.txt
├── .env.sample
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
│   ├── blog/                   # Blog app
│   │   ├── __init__.py
│   │   ├── admin.py            # Admin interface configuration
│   │   ├── apps.py             # App configuration
│   │   ├── models.py           # Data models (Post, Comment, Category)
│   │   ├── serializers.py      # DRF serializers
│   │   ├── urls.py             # URL routing
│   │   ├── views.py            # API views and viewsets
│   │   ├── tests/              # Tests directory
│   │   │   ├── __init__.py
│   │   │   ├── test_models.py  # Model tests
│   │   │   ├── test_views.py   # API tests
│
├── templates/                  # HTML templates
│   ├── django_filters/         # Templates for django-filter
│
├── static/                     # Static files
├── media/                      # Media files (user uploads)
│
├── scripts/                    # Custom management/utility scripts
│
└── docker/                     # Docker config
    ├── Dockerfile              # Container definition
    └── docker-compose.yml      # Service configuration
```

## Getting Started

### Using Docker (Recommended)

1. Clone the repository:
```bash
git clone https://github.com/sunilsingh2019/Finsure-Blog-Platform.git
cd Finsure-Blog-Platform
```

2. Create `.env` file from example:
```bash
cp .env.sample .env
```

3. Build and run the Docker containers:
```bash
cd docker
docker-compose up --build
```

4. Create database migrations:
```bash
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate
```

5. Create a superuser (optional):
```bash
docker-compose exec web python manage.py createsuperuser
```

### Without Docker

1. Clone the repository:
```bash
git clone https://github.com/sunilsingh2019/Finsure-Blog-Platform.git
cd Finsure-Blog-Platform
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create `.env` file from example:
```bash
cp .env.sample .env
```

4. Set up PostgreSQL:
   - Install PostgreSQL if not already installed
   - Create a database for the project
   - Update .env with your database credentials

5. Set up the database:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Run the development server:
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
- `GET /api/posts/`: List all blog posts (paginated, 5 per page)
- `GET /api/posts/{id}/`: Get details of a specific post
- `PUT /api/posts/{id}/`: Update a post
- `DELETE /api/posts/{id}/`: Delete a post
- `POST /api/posts/{id}/like/`: Like a post
- `POST /api/posts/{id}/dislike/`: Dislike a post

### Comments

- `POST /api/posts/{post_id}/comments/`: Create a comment on a post
- `GET /api/posts/{post_id}/comments/`: List all comments for a post
- `GET /api/posts/{post_id}/comments/{id}/`: Get details of a specific comment
- `PUT /api/posts/{post_id}/comments/{id}/`: Update a comment
- `DELETE /api/posts/{post_id}/comments/{id}/`: Delete a comment

### Categories

- `POST /api/categories/`: Create a new category
- `GET /api/categories/`: List all categories
- `GET /api/categories/{id}/`: Get details of a specific category
- `PUT /api/categories/{id}/`: Update a category
- `DELETE /api/categories/{id}/`: Delete a category

## Filtering and Searching

The API supports various filtering and searching options:

- **Filter posts by author**: 
  ```
  GET /api/posts/?author=JohnDoe
  ```

- **Filter posts by category**: 
  ```
  GET /api/posts/?categories=1
  ```

- **Search in post titles and content**: 
  ```
  GET /api/posts/?search=django
  ```

- **Order posts by various fields**: 
  ```
  GET /api/posts/?ordering=-created_at
  GET /api/posts/?ordering=title
  GET /api/posts/?ordering=-likes
  ```

## Pagination

The API uses page-based pagination with 5 items per page:

- **View first page**:
  ```
  GET /api/posts/
  ```

- **View specific page**:
  ```
  GET /api/posts/?page=2
  ```

- The response includes:
  - `count`: Total number of items
  - `next`: URL to the next page (null if on last page)
  - `previous`: URL to the previous page (null if on first page)
  - `results`: List of items on the current page

## Running Tests

The project includes comprehensive tests covering models, API endpoints, permissions, and pagination.

```bash
# Using Docker
docker-compose exec web python manage.py test

# Without Docker
python manage.py test
```

## Admin Interface

The Django admin interface is available at `/admin/` and provides a user-friendly way to manage all content.

## Future Enhancements

Potential future improvements:
- User authentication with JWT tokens
- User profiles and avatars
- Rich text support for posts
- Image uploads for posts
- Tags system
- Newsletter subscription
- Comment threading

## License

This project is licensed under the MIT License - see the LICENSE file for details. 