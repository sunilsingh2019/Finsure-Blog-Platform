#!/bin/bash

# Initialize project
echo "Setting up Blog Platform API..."

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
fi

# Create necessary directories
echo "Creating directories..."
mkdir -p static media templates

# Run migrations
echo "Running migrations..."
python manage.py makemigrations blog
python manage.py migrate

echo "Setup complete!"
echo "You can now run the server using:"
echo "python manage.py runserver" 