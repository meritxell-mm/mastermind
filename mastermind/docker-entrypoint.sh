#!/bin/bash
sleep 10 #wait for postgres to be ready
cd /code
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000