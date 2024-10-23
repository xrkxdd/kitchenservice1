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

# Check if Gunicorn is installed and use full path if necessary
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn could not be found. Installing Gunicorn..."
    python3 -m pip install gunicorn
fi

# Find the path to Gunicorn in case it's not in PATH
GUNICORN_PATH=$(command -v gunicorn)
if [ -z "$GUNICORN_PATH" ]; then
    echo "Gunicorn is still not found after installation!"
    exit 1
fi

# Start Gunicorn server with full path
echo "Starting Gunicorn server..."
$GUNICORN_PATH kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
