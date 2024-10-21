#!/usr/bin/env bash
# Exit on error
set -o errexit

# Print Python version
echo "Using Python version:"
python3 --version || { echo "Python 3 is not installed or not found!"; exit 1; }

<<<<<<< HEAD
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
=======
# Add Poetry to the PATH
export PATH="/opt/render/project/poetry/bin:$PATH"

# Print Poetry version
echo "Using Poetry version:"
/opt/render/project/poetry/bin/poetry --version || { echo "Poetry is not installed or not found!"; exit 1; }

# Upgrade pip
echo "Upgrading pip..."
python3 -m pip install --upgrade pip

# Install dependencies using Poetry
echo "Installing dependencies..."
/opt/render/project/poetry/bin/poetry install

# Convert static asset files
echo "Collecting static files..."
/opt/render/project/poetry/bin/poetry run python3 manage.py collectstatic --no-input

# Apply any outstanding database migrations
echo "Applying migrations..."
/opt/render/project/poetry/bin/poetry run python3 manage.py migrate

# Check if Gunicorn is installed
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn could not be found. Please ensure it is installed."
    exit 1
>>>>>>> d6764e5adc425d938e90d90edbc8619ddd5209cf
fi

# Start Gunicorn server
echo "Starting Gunicorn server..."
<<<<<<< HEAD
gunicorn kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
=======
/opt/render/project/poetry/bin/poetry run gunicorn kitchenservice.wsgi:application --bind 0.0.0.0:$PORT
>>>>>>> d6764e5adc425d938e90d90edbc8619ddd5209cf
