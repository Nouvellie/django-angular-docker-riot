#!/bin/bash
python manage.py migrate --noinput
python manage.py collectstatic --no-input --clear
gunicorn main.wsgi:application --workers 4 --preload --timeout 3600 --bind 0.0.0.0:8000