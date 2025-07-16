#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z $DB_HOST 5432; do
  sleep 0.1
done

echo "PostgreSQL started"
sleep 2

python manage.py collectstatic --no-input
python manage.py migrate --no-input

gunicorn -w 1 mysite.wsgi -b 0.0.0.0:8000