# Developer Documentation for Blog Platform API

This document provides detailed technical information about the Blog Platform API for developers who want to understand, maintain, or extend the codebase.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Technology Stack](#technology-stack)
3. [Project Structure](#project-structure)
4. [Data Models](#data-models)
5. [API Design](#api-design)
6. [Authentication and Permissions](#authentication-and-permissions)
7. [Serializers](#serializers)
8. [ViewSets and Views](#viewsets-and-views)
9. [URL Routing](#url-routing)
10. [Filtering and Searching](#filtering-and-searching)
11. [Pagination](#pagination)
12. [Testing](#testing)
13. [Docker Setup](#docker-setup)
14. [Development Workflow](#development-workflow)
15. [Adding New Features](#adding-new-features)
16. [Code Style Guide](#code-style-guide)

## Architecture Overview

The Blog Platform API follows a typical Django REST Framework architecture, with the following components:

- **Models**: Define the database schema and business logic
- **Serializers**: Handle data conversion between Python objects and JSON
- **Views**: Process HTTP requests and return responses
- **URLs**: Map URLs to views
- **Settings**: Configure the application

The application uses a modular design with a clear separation of concerns:

- **apps/**: Contains the Django applications
- **config/**: Houses project-wide settings and configuration
- **docker/**: Contains Docker configuration for deployment
- **static/ and media/**: Store static assets and user uploads
- **templates/**: Contains HTML templates for rendering

## Technology Stack

- **Python 3.11**: Programming language
- **Django 5.1.8**: Web framework
- **Django REST Framework 3.15.0**: REST API framework
- **PostgreSQL 15**: Database
- **django-filter 24.1**: Filtering backend
- **drf-yasg 1.21.7**: Swagger/OpenAPI documentation
- **Whitenoise 6.6.0**: Static file serving
- **Docker & Docker Compose**: Containerization
- **Gunicorn 21.2.0**: WSGI HTTP Server
- **Python-decouple 3.8**: Configuration management

## Project Structure

```
├── apps/                       # Django applications
│   ├── __init__.py             # Makes apps a Python package
│   ├── blog/                   # Blog application
│       ├── __init__.py         # Makes blog a Python package
│       ├── admin.py            # Admin interface models registration
│       ├── apps.py             # App configuration
│       ├── models.py           # Data models
│       ├── serializers.py      # JSON serializers/deserializers
│       ├── urls.py             # URL routing for blog app
│       ├── views.py            # Views and viewsets
│       ├── migrations/         # Database migrations
│       ├── tests/              # Tests directory
│           ├── __init__.py     # Makes tests a package
│           ├── test_models.py  # Tests for models
│           ├── test_views.py   # Tests for views/API
│
├── config/                     # Project configuration
│   ├── __init__.py             # Makes config a Python package
│   ├── asgi.py                 # ASGI configuration
│   ├── urls.py                 # Project-level URL routing
│   ├── wsgi.py                 # WSGI configuration
│   ├── settings/               # Settings modules
│       ├── __init__.py         # Settings package
│       ├── base.py             # Base settings
│       ├── development.py      # Development-specific settings
│       ├── production.py       # Production-specific settings
│
├── docker/                     # Docker configuration
│   ├── Dockerfile              # Docker image definition
│   ├── docker-compose.yml      # Docker Compose services
│
├── static/                     # Static files
├── media/                      # Media files (uploads)
├── templates/                  # HTML templates
│   ├── django_filters/         # Templates for django-filter
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── README.md                   # Project overview
└── .gitignore                  # Git ignored files
```

## Data Models

The project uses three primary models:

### Category Model

```python
class Category(models.Model):
    """Model for blog post categories"""
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name
```

### Post Model

```python
class Post(models.Model):
    """Model for blog posts"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=255)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title
```

### Comment Model

```python
class Comment(models.Model):
    """Model for comments on blog posts"""
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=255)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"
```

## API Design

The API follows RESTful principles with resource-based URLs, appropriate HTTP methods, and nested resources where relevant.

### Endpoints Structure

- `/api/posts/`: Post collection resource
- `/api/posts/{id}/`: Post instance resource
- `/api/posts/{id}/like/`: Action on a post
- `/api/posts/{id}/dislike/`: Action on a post
- `/api/posts/{post_id}/comments/`: Nested comment collection for a post
- `/api/posts/{post_id}/comments/{id}/`: Nested comment instance
- `/api/categories/`: Category collection resource
- `/api/categories/{id}/`: Category instance resource

### HTTP Methods

- **GET**: Retrieve a resource or collection
- **POST**: Create a new resource
- **PUT**: Update an entire resource
- **DELETE**: Remove a resource

## Authentication and Permissions

Currently, the API uses Django REST Framework's `AllowAny` permission, which allows unrestricted access to all endpoints. This is configured in `config/settings/base.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    # ...
}
```

To implement more restrictive permissions:

1. Create custom permission classes in a new file (e.g., `apps/blog/permissions.py`)
2. Use those permission classes in your views:

```python
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    # ...
```

## Serializers

Serializers handle conversion between Python objects and JSON representations.

### Key Serializers

- **CategorySerializer**: Handles Category model (de)serialization
- **PostSerializer**: Handles Post model (de)serialization with nested categories
- **PostListSerializer**: Simplified serializer for listing posts
- **CommentSerializer**: Handles Comment model (de)serialization
- **CommentListSerializer**: Simplified serializer for listing comments
- **CommentDetailSerializer**: Serializer for detailed comment views

### Custom Serializer Features

The `PostSerializer` includes a `category_ids` write-only field for associating categories with posts:

```python
class PostSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        many=True,
        write_only=True,
        required=False,
        source='categories'
    )
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 
                  'categories', 'category_ids', 'likes', 'dislikes']
        read_only_fields = ['id', 'created_at', 'updated_at', 'likes', 'dislikes']
```

## ViewSets and Views

The application uses a mix of ViewSets and generic views:

### ViewSets

- **CategoryViewSet**: CRUD operations for categories
- **PostViewSet**: CRUD operations for posts, with custom actions for like/dislike

```python
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['author', 'categories']
    search_fields = ['title', 'content', 'author']
    ordering_fields = ['created_at', 'updated_at', 'title', 'likes', 'dislikes']
    template_name = None  # Disable template rendering for filters
    
    def get_serializer_class(self):
        if self.action == 'list':
            return PostListSerializer
        return PostSerializer
    
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        """Endpoint to like a post"""
        post = self.get_object()
        post.likes += 1
        post.save()
        return Response({'status': 'post liked', 'likes': post.likes})
```

### Generic Views

- **CommentCreateListView**: List/create comments for a post
- **CommentDetailView**: Retrieve/update/delete a specific comment

```python
class CommentCreateListView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    
    def get_queryset(self):
        post_id = self.kwargs['post_id']
        return Comment.objects.filter(post_id=post_id)
    
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return CommentListSerializer
        return CommentSerializer
```

## URL Routing

URL routing is handled at two levels:

### Project-level URLs (`config/urls.py`)

```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.blog.urls')),
    
    # Swagger documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
```

### App-level URLs (`apps/blog/urls.py`)

```python
router = DefaultRouter()
router.register(r'posts', PostViewSet)
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    # Comment URLs
    path('posts/<int:post_id>/comments/', CommentCreateListView.as_view(), name='comment-list-create'),
    path('posts/<int:post_id>/comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
]

# Add router URLs to urlpatterns
urlpatterns += router.urls
```

## Filtering and Searching

The project uses django-filter for filtering and DRF's built-in search functionality:

```python
# In views.py
filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
filterset_fields = ['author', 'categories']
search_fields = ['title', 'content', 'author']
ordering_fields = ['created_at', 'updated_at', 'title', 'likes', 'dislikes']
```

To use filtering:
- `/api/posts/?author=JohnDoe`: Filter by author
- `/api/posts/?categories=1`: Filter by category
- `/api/posts/?search=django`: Search in title, content, and author
- `/api/posts/?ordering=-created_at`: Order by creation date (descending)

To add additional filters, update the `filterset_fields` list in the viewset.

## Pagination

Pagination is configured globally in the settings:

```python
REST_FRAMEWORK = {
    # ...
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 5,
    # ...
}
```

Custom pagination classes can be created and applied either globally or to specific viewsets:

```python
# Example of a custom pagination class
class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

# Applying to a viewset
class PostViewSet(viewsets.ModelViewSet):
    pagination_class = CustomPagination
    # ...
```

## Testing

The project uses Django's `TestCase` and DRF's `APITestCase` for testing:

### Model Tests

Tests for data integrity, relationships, and methods:

```python
class CategoryModelTest(TestCase):
    def setUp(self):
        Category.objects.create(
            name="Test Category",
            description="This is a test category."
        )

    def test_category_creation(self):
        category = Category.objects.get(name="Test Category")
        self.assertEqual(category.description, "This is a test category.")
        self.assertTrue(category.created_at)
```

### API Tests

Tests for API endpoints, requests, responses, and business logic:

```python
class PostAPITests(APITestCase):
    def test_create_post(self):
        data = {'title': 'New Post', 'content': 'New Content', 'author': 'New Author'}
        response = self.client.post(self.list_create_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 3)
        self.assertEqual(Post.objects.get(title='New Post').author, 'New Author')
```

### Running Tests

```bash
# Run all tests
python manage.py test

# Run specific test case
python manage.py test apps.blog.tests.test_views.PostAPITests

# Run specific test method
python manage.py test apps.blog.tests.test_views.PostAPITests.test_create_post
```

## Docker Setup

The project uses Docker for containerization:

### Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_ENVIRONMENT=development

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### docker-compose.yml

```yaml
services:
  web:
    build:
      context: ..
      dockerfile: ./docker/Dockerfile
    command: python manage.py runserver 0.0.0.0:8000
    volumes:
      - ..:/app
    ports:
      - "8000:8000"
    depends_on:
      - db
    env_file:
      - ../.env
    environment:
      - DEBUG=True
      - DJANGO_ENVIRONMENT=development

  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    environment:
      - POSTGRES_PASSWORD=postgres
      - POSTGRES_USER=postgres
      - POSTGRES_DB=postgres
    ports:
      - "5433:5432"
```

## Development Workflow

### Setting Up a Development Environment

1. Clone the repository
2. Set up Docker or a local Python environment
3. Install dependencies
4. Run migrations
5. Start the development server

### Making Changes

1. Create a feature branch: `git checkout -b feature/your-feature-name`
2. Make changes to the code
3. Run tests to ensure everything works: `python manage.py test`
4. Commit changes: `git commit -m "Add your feature"`
5. Push to the branch: `git push origin feature/your-feature-name`
6. Create a pull request

## Adding New Features

### Adding a New Model

1. Define the model in `apps/blog/models.py`:
```python
class NewModel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
```

2. Create and run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Register in admin (`apps/blog/admin.py`):
```python
@admin.register(NewModel)
class NewModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
```

### Adding a New API Endpoint

1. Create a serializer in `apps/blog/serializers.py`:
```python
class NewModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewModel
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
```

2. Create a viewset in `apps/blog/views.py`:
```python
class NewModelViewSet(viewsets.ModelViewSet):
    queryset = NewModel.objects.all()
    serializer_class = NewModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name', 'description']
```

3. Add to URL router in `apps/blog/urls.py`:
```python
router.register(r'new-models', NewModelViewSet)
```

4. Add tests for the new feature

## Code Style Guide

The project follows Python's PEP 8 style guide with the following additions:

### General Guidelines

- Use 4 spaces for indentation
- Use docstrings for all classes and methods
- Keep lines to a maximum of 100 characters
- Use meaningful variable and function names
- Use comments to explain complex logic

### Django-Specific Guidelines

- Use descriptive names for models, fields, and views
- Group model fields logically
- Use the `related_name` attribute for reverse relationships
- Keep views focused on a single responsibility
- Use Django's ORM methods rather than raw SQL when possible
- Follow Django's security best practices

### Testing Guidelines

- Write tests for all models and API endpoints
- Use descriptive test method names that explain what is being tested
- Follow the Arrange-Act-Assert pattern
- Keep tests isolated and independent
- Mock external services and dependencies

By following these guidelines, you can contribute to the project effectively while maintaining code quality and consistency. 