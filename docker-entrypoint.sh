#!/bin/sh

set -e

echo "Waiting for database..."

# DB wait loop (important for docker-compose dev setups)
until python manage.py migrate --noinput 2>/dev/null; do
  echo "DB not ready yet, retrying..."
  sleep 2
done

echo "Database ready."

echo "Starting Django server..."

exec python manage.py runserver 0.0.0.0:8000
