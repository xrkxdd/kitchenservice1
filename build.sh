#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies using Poetry
poetry install

# Convert static asset files
poetry run python manage.py collectstatic --no-input

# Apply any outstanding database migrations
poetry run python manage.py migrate

# Start Gunicorn server
poetry run gunicorn kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
