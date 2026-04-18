#! /bin/bash

export DJANGO_SUPERUSER_PASSWORD=Imaging-Deferred4-Unaltered
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py createsuperuser --username admin --email admin@django.site --no-input
uv run manage.py collectstatic --no-input
uv run main.py
