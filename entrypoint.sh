#!/bin/bash

# Wait for the database to be ready (adjust parameters as needed)
python /code/wait_for_db.py

# Apply migrations (if needed)
python manage.py migrate

# Import data
python manage.py import_data

# Start the Django development server or your preferred process
exec "$@"