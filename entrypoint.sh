#!/bin/bash

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py flush --no-input
python manage.py migrate
# Collect static files from app and puts to STATIC_ROOT
python manage.py collectstatic --no-input
# Seeds
python3 manage.py fill_db 10

exec "$@"
