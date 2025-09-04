#!/bin/bash

# Exit on any error
set -e

echo "Starting Django application..."

# Run migrations
echo "Running database migrations..."
python manage.py migrate --noinput

# Collect static files (only if not disabled)
if [ "${DISABLE_COLLECTSTATIC}" != "1" ]; then
    echo "Collecting static files..."
    python manage.py collectstatic --noinput
else
    echo "Static file collection disabled"
fi

# Create default superuser if it doesn't exist
echo "Creating default superuser if needed..."
python manage.py create_default_superuser

# Start the application
echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:$PORT --workers 3 agri_project.wsgi:application
