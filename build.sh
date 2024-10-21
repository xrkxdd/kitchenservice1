#!/usr/bin/env bash
# Exit on error
set -o errexit

# Print Python version
echo "Using Python version:"
python3 --version || { echo "Python 3 is not installed or not found!"; exit 1; }

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies using requirements.txt
echo "Installing dependencies..."
python3 -m pip install -r requirements.txt

# Convert static asset files
echo "Collecting static files..."
python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
echo "Applying migrations..."
python3 manage.py migrate

# Check if Gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn could not be found. Installing Gunicorn..."
    python3 -m pip install gunicorn
fi

# Start Gunicorn server
echo "Starting Gunicorn server..."
gunicorn kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
