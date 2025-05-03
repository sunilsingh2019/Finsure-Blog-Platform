# Django REST Framework Boilerplate

A modern Django REST Framework boilerplate with Docker support.

## Features

- Django 5.1.7
- Django REST Framework 3.15.0
- PostgreSQL database
- Swagger API documentation
- Docker and Docker Compose ready
- Custom User model with email authentication
- WhiteNoise for static files
- RESTful API structure

## Requirements

- Docker
- Docker Compose

## Quick Start

1. Clone this repository
2. Create a `.env` file (copy from `.env.example`)
3. Build and run the Docker containers:

```bash
docker compose up --build
```

4. The application will be available at http://localhost:8000/

## API Documentation

- Swagger UI: http://localhost:8000/
- ReDoc: http://localhost:8000/redoc/

## Project Structure

```
.
├── apps                   # Django applications
│   ├── api                # API related code
│   ├── core               # Core application
│   └── users              # User management
├── core                   # Django project settings
├── static                 # Static files
├── media                  # User-uploaded content
├── templates              # HTML templates
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile             # Docker configuration
├── manage.py              # Django command-line utility
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies
```

## Commands

### Running the Application

```bash
docker compose up
```

### Creating a Superuser

```bash
docker compose exec web python manage.py createsuperuser
```

### Running Migrations

```bash
docker compose exec web python manage.py migrate
```

### Collecting Static Files

```bash
docker compose exec web python manage.py collectstatic --noinput
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 