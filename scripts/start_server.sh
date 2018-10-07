#!/usr/bin/env bash

# create DB (and run migrations)
./django_drf/manage.py migrate
./django_drf/manage.py populate
./django_drf/manage.py runserver 0.0.0.0:8000

