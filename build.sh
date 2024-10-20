#!/usr/bin/env bash
# Exit on error
set -o errexit

# Print Python and Poetry versions
echo "Using Python version:"
python3 --version

echo "Using Poetry version:"
poetry --version

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python could not be found. Please ensure Python is installed."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies using Poetry
echo "Installing dependencies..."
poetry install

# Convert static asset files
echo "Collecting static files..."
poetry run python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
echo "Applying migrations..."
poetry run python3 manage.py migrate

# Check if Gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn could not be found. Please ensure it is installed."
    exit 1
fi

# Start Gunicorn server
echo "Starting Gunicorn server..."
poetry run gunicorn kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
