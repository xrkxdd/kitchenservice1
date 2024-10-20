#!/usr/bin/env bash
# Exit on error
set -o errexit

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. Please ensure Python is installed."
    exit 1
fi

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    python3 -m pip install -r requirements.txt
else
    echo "requirements.txt not found! Please ensure it exists."
    exit 1
fi

# Convert static asset files
python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
python3 manage.py migrate

# Start Gunicorn server
gunicorn kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
