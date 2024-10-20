#!/usr/bin/env bash
# Exit on error
set -o errexit

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. Please ensure Python is installed."
    exit 1
fi

# Install dependencies using Poetry
poetry install

# Convert static asset files
poetry run python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
poetry run python3 manage.py migrate

# Start Gunicorn server
poetry run gunicorn kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
