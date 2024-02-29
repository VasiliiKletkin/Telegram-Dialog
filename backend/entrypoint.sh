#!/bin/sh

sleep 2
python manage.py migrate
# python manage.py collectstatic --noinput

exec "$@"