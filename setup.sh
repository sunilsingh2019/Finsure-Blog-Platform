#!/bin/bash

# Create the Django project
echo "Creating Django project..."
django-admin startproject core .

# Create base apps
echo "Creating apps..."
mkdir -p apps
touch apps/__init__.py
python manage.py startapp api apps/api
python manage.py startapp users apps/users

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Create necessary directories
mkdir -p static media templates

echo "Setup complete!" 